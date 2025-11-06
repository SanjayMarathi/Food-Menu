from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F, DecimalField # Used for dashboard reports

# QR Code Libraries
import qrcode
from io import BytesIO
from base64 import b64encode

# Import models and forms
from .models import Item, Order, OrderItem
from .forms import ItemForm

# --- Permissions Helper ---
def staff_required(view_func):
    """Decorator to ensure user is logged in AND is staff."""
    @login_required(login_url='login')
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper

# --- Admin/Staff Views ---

@staff_required
def index(request):
    """Staff Menu Management List (Shows ALL items, including unavailable)"""
    item_list = Item.objects.all()
    context = {
        'item_list':item_list
    }
    return render(request,"myapp/index.html",context)

@staff_required
def detail(request, id):
    item = get_object_or_404(Item, id=id)
    return render(request, 'myapp/detail.html', {'item':item})
      
@staff_required
def create_item(request):
    form = ItemForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        item = form.save(commit=False)
        item.user_name = request.user
        item.save()
        return redirect('myapp:index')
    return render(request, 'myapp/item_form.html', {'form': form, 'title': 'Add New Food Item'})

@staff_required
def update_item(request, id):
    item = get_object_or_404(Item, id=id)
    form = ItemForm(request.POST or None, instance = item)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('myapp:detail', id=item.id)
    return render(request, 'myapp/item_form.html', {'form':form, 'item': item, 'title': f'Update {item.item_name}'})

@staff_required
def delete_item(request, id): 
    item = get_object_or_404(Item, id=id)
    if request.method == 'POST':
        item.delete()
        return redirect('myapp:index')
    return render(request, 'myapp/item_delete.html', {'item': item})

# --- QR Code and Dashboard Logic ---

@staff_required
def staff_dashboard(request):
    """Dashboard for staff to view orders, revenue, and item sales."""
    
    active_orders = Order.objects.filter(status__in=['Pending', 'Preparing']).order_by('-created_at')
    
    all_orders = Order.objects.all()
    total_orders_count = all_orders.count()
    total_revenue = all_orders.filter(is_paid=True).aggregate(total=Sum('total_price'))['total'] or 0.00
    
    item_sales_report = OrderItem.objects.values('item_name').annotate(
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


@staff_required
def generate_qr_code(request, table_id):
    """Generates a QR code for a specific table URL."""
    # Construct the full URL that the QR code should point to
    relative_url = reverse('myapp:menu_with_table', kwargs={'table_id': table_id})
    full_url = request.build_absolute_uri(relative_url)

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

# Placeholder for Order Status Update (Staff action)
@staff_required
def update_order_status(request, order_id, new_status):
    order = get_object_or_404(Order, id=order_id)
    if new_status in [choice[0] for choice in Order.STATUS_CHOICES]:
        order.status = new_status
        if new_status == 'Completed':
            order.is_paid = True
        order.save()
    return redirect('myapp:staff_dashboard')


# --- Customer Facing Views (The functions that were missing) ---

def menu(request, table_id=None):
    """Public view for customers, filters items by is_available=True."""
    if table_id:
        request.session['table_number'] = table_id
    
    # FIX: Apply availability filter
    item_list = Item.objects.filter(is_available=True)
    context = {
        'item_list': item_list,
        'table_number': request.session.get('table_number', 'N/A')
    }
    return render(request, 'myapp/menu.html', context)

def add_to_cart(request, item_id):
    """Handles adding item to session-based cart."""
    item = get_object_or_404(Item, id=item_id)
    cart = request.session.get('cart', {})
    
    item_id_str = str(item_id)
    
    if item_id_str in cart:
        cart[item_id_str]['quantity'] += 1
    else:
        cart[item_id_str] = {
            'name': item.item_name,
            'price': float(item.item_price),
            'quantity': 1
        }
        
    request.session['cart'] = cart
    return redirect('myapp:view_cart')

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
        
        return render(request, 'myapp/checkout_success.html', {'order': new_order})
        
    return redirect('myapp:view_cart')