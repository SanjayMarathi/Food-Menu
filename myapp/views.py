from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F, DecimalField # Used for dashboard reports
from django.contrib import messages 

# QR Code Libraries
import qrcode
from io import BytesIO
from base64 import b64encode

# Import models and forms
from .models import Item, Order, OrderItem
from .forms import ItemForm

# --- Admin/Staff Views (Now Multi-Tenant by filtering by request.user) ---

@login_required(login_url='login')
def index(request):
    """Staff Menu Management List (Shows ONLY items created by the logged-in user)"""
    # FILTER: Only show items created by the current user
    item_list = Item.objects.filter(user_name=request.user)
    context = {
        'item_list':item_list
    }
    return render(request,"myapp/index.html",context)

@login_required(login_url='login')
def detail(request, id):
    # FILTER: Only get item if it belongs to the current user
    item = get_object_or_404(Item, id=id, user_name=request.user)
    return render(request, 'myapp/detail.html', {'item':item})
      
@login_required(login_url='login')
def create_item(request):
    form = ItemForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        item = form.save(commit=False)
        # ASSIGN: Set the creator of the item to the current user
        item.user_name = request.user
        item.save()
        return redirect('myapp:index')
    return render(request, 'myapp/item_form.html', {'form': form, 'title': 'Add New Food Item'})

@login_required(login_url='login')
def update_item(request, id):
    # FILTER: Only get item if it belongs to the current user
    item = get_object_or_404(Item, id=id, user_name=request.user)
    form = ItemForm(request.POST or None, instance = item)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('myapp:detail', id=item.id)
    return render(request, 'myapp/item_form.html', {'form':form, 'item': item, 'title': f'Update {item.item_name}'})

@login_required(login_url='login')
def delete_item(request, id): 
    # FILTER: Only get item if it belongs to the current user
    item = get_object_or_404(Item, id=id, user_name=request.user)
    if request.method == 'POST':
        item.delete()
        return redirect('myapp:index')
    return render(request, 'myapp/item_delete.html', {'item': item})

# --- QR Code and Dashboard Logic ---

@login_required(login_url='login')
def staff_dashboard(request):
    """Dashboard for staff to view orders, revenue, and item sales FOR THEIR RESTAURANT."""
    
    # 1. Base query: Orders that contain items owned by the current user
    all_orders_for_user = Order.objects.filter(
        orderitem__item__user_name=request.user
    ).distinct()

    # 2. Active Orders
    active_orders = all_orders_for_user.filter(
        status__in=['Pending', 'Preparing']
    ).order_by('-created_at')
    
    # 3. Totals and Revenue
    total_orders_count = all_orders_for_user.count()
    total_revenue = all_orders_for_user.filter(
        is_paid=True
    ).aggregate(
        total=Sum('total_price')
    )['total'] or 0.00
    
    # 4. Item Sales Report (Filter OrderItems by the Item's owner)
    item_sales_report = OrderItem.objects.filter(
        item__user_name=request.user,
        order__is_paid=True # Only count paid orders for revenue/sales report
    ).values('item_name').annotate(
        total_quantity=Sum('quantity'),
        total_revenue=Sum(F('item_price') * F('quantity'), output_field=DecimalField())
    ).order_by('-total_quantity')
    
    context = {
        'active_orders': active_orders,
        'total_orders_count': total_orders_count,
        'total_revenue': total_revenue,
        'item_sales_report': item_sales_report,
    }
    return render(request, 'myapp/staff_dashboard.html', context)


@login_required(login_url='login')
def generate_qr_code(request, table_id):
    """Generates a QR code for a specific table URL."""
    # UPDATED: Include the staff user's username in the URL so the menu view can filter.
    username = request.user.username
    relative_url = reverse('myapp:menu_with_table', kwargs={'username': username, 'table_id': table_id})
    full_url = request.build_absolute_uri(relative_url)

    # ... (rest of the QR code generation logic remains the same)

    # 1. Create QR code object
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(full_url)
    qr.make(fit=True)

    # 2. Create an image from the QR code and save to a buffer
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    
    # 3. Encode the image data to Base64
    qr_code_base64 = b64encode(buffer.getvalue()).decode('utf-8')

    context = {
        'table_id': table_id,
        'qr_code_data': qr_code_base64,
        'full_url': full_url
    }
    return render(request, 'myapp/qr_generator.html', context)

@login_required(login_url='login')
def update_order_status(request, order_id, new_status):
    # FILTER: Only allow updating orders that contain items owned by the current user
    order = get_object_or_404(
        Order.objects.filter(orderitem__item__user_name=request.user).distinct(), 
        id=order_id
    )

    if new_status in [choice[0] for choice in Item.STATUS_CHOICES]:
        order.status = new_status
        if new_status == 'Completed':
            order.is_paid = True
        order.save()
    return redirect('myapp:staff_dashboard')


# --- Customer Facing Views (Public menu now filters by item availability, NOT ownership) ---

def menu(request, username=None, table_id=None):
    """Public view for customers, filters items by is_available=True AND optionally by a restaurant/user if provided in the URL."""
    if table_id:
        request.session['table_number'] = table_id
        # Store the current menu URL for redirection after adding an item to cart
        # UPDATED: Pass the username to the redirect URL
        request.session['menu_redirect_url'] = reverse('myapp:menu_with_table', kwargs={'username': username, 'table_id': table_id})
    else:
        # Clear the table-specific redirect URL if accessing the root menu
        if 'menu_redirect_url' in request.session:
            del request.session['menu_redirect_url']
    
    # Filter items:
    # 1. Always filter by is_available=True
    item_list = Item.objects.filter(is_available=True)
    
    # 2. If a username is provided in the URL (from a QR scan), filter by that user's items.
    if username:
        item_list = item_list.filter(user_name__username=username) # Filter by the username from the URL

    context = {
        'item_list': item_list,
        'table_number': request.session.get('table_number', 'N/A')
    }
    return render(request, 'myapp/menu.html', context)

def add_to_cart(request, item_id):
    """Handles adding item to session-based cart, redirects back to menu with a message."""
    item = get_object_or_404(Item, id=item_id)
    cart = request.session.get('cart', {})
    
    item_id_str = str(item_id)
    
    if item_id_str in cart:
        cart[item_id_str]['quantity'] += 1
    else:
        cart[item_id_str] = {
            'name': item.item_name,
            'price': float(item.item_price),
            'quantity': 1,
            'description': item.item_description # <--- ADDED
        }
        
    request.session['cart'] = cart
    
    # Add success message (Notification type)
    messages.success(request, f"{item.item_name} added to cart!")

    # Redirect back to the menu (main or table-specific)
    menu_redirect_url = request.session.get('menu_redirect_url', reverse('myapp:menu'))
    return redirect(menu_redirect_url) # <--- REDIRECT CHANGED

def view_cart(request):
    """Displays the current cart contents."""
    cart = request.session.get('cart', {})
    cart_items = cart.values()
    cart_total = sum(item['price'] * item['quantity'] for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'table_number': request.session.get('table_number', 'N/A')
    }
    return render(request, 'myapp/cart.html', context)

def checkout(request):
    """Creates a new Order from the cart and clears the cart."""
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('myapp:menu')

    if request.method == 'POST':
        cart_total = sum(item['price'] * item['quantity'] for item in cart.values())
        
        new_order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            table_number=request.session.get('table_number'),
            total_price=cart_total,
            status='Pending',
            is_paid=False
        )

        order_items = []
        for item_id_str, item_data in cart.items():
            item_id = int(item_id_str)
            item_instance = Item.objects.filter(id=item_id).first()
            order_items.append(OrderItem(
                order=new_order,
                item=item_instance,
                item_name=item_data['name'],
                item_price=item_data['price'],
                quantity=item_data['quantity']
            ))
        OrderItem.objects.bulk_create(order_items)
        
        del request.session['cart']
        
        # FIX: Get the correct menu redirect URL from session, default to generic menu
        menu_redirect_url = request.session.get('menu_redirect_url', reverse('myapp:menu'))
        
        return render(request, 'myapp/checkout_success.html', {
            'order': new_order,
            'menu_redirect_url': menu_redirect_url # Pass URL to template
        })
        
    return redirect('myapp:view_cart')