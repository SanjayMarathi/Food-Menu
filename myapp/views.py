from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Item, Order, OrderItem # Import new models
from .forms import ItemForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Sum, Count, F, DecimalField # For reporting
import json # For cart session data

# --- Permissions Helper ---
def staff_required(view_func):
    """Decorator to ensure user is logged in AND is staff."""
    @login_required(login_url='login')
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper

# --- Admin/Staff Views (Menu Management) ---

@staff_required
def index(request):
    # This view is now for Staff to manage items (Read/List View)
    item_list = Item.objects.all()
    context = {
        'item_list':item_list
    }
    return render(request,"myapp/index.html",context)

# Item Detail View (Should only be accessed by staff for management)
@staff_required
def detail(request, id):
    item = get_object_or_404(Item, id=id)
    return render(request, 'myapp/detail.html', {
        'item':item
    })
      
# Create Item View
@staff_required
def create_item(request):
    form = ItemForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            item = form.save(commit=False)
            item.user_name = request.user
            item.save()
            return redirect('myapp:index')

    context = {
        'form': form,
        'title': 'Add New Food Item'
    }
    return render(request, 'myapp/item_form.html', context)

# Update Item View
@staff_required
def update_item(request, id):
    item = get_object_or_404(Item, id=id)
    form = ItemForm(request.POST or None, instance = item)
    if request.method == 'POST': 
        if form.is_valid():
            form.save()
            return redirect('myapp:detail', id=item.id)
            
    context = {
        'form':form,
        'item': item,
        'title': f'Update {item.item_name}'
    }
    return render(request, 'myapp/item_form.html', context)

# Delete Item View
@staff_required
def delete_item(request, id): 
    item = get_object_or_404(Item, id=id)
    if request.method == 'POST':
        item.delete()
        return redirect('myapp:index')
        
    context = {
        'item': item
    }
    return render(request, 'myapp/item_delete.html', context)
    
# --- Customer Facing Views (Ordering Flow) ---

def menu(request, table_id=None):
    """Public view for customers (simulating QR scan access)."""
    # Optional: store table_id in session for the order
    if table_id:
        request.session['table_number'] = table_id
    
    item_list = Item.objects.all()
    context = {
        'item_list': item_list,
        'table_number': request.session.get('table_number', 'N/A')
    }
    return render(request, 'myapp/menu.html', context)

def add_to_cart(request, item_id):
    """Handles adding item to session-based cart."""
    item = get_object_or_404(Item, id=item_id)
    cart = request.session.get('cart', {})
    
    # Cart structure: {'item_id': {'name': 'Pizza', 'price': 10, 'quantity': 1}}
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
        return redirect('myapp:menu') # No items in cart

    if request.method == 'POST':
        # 1. Create the Order object
        cart_total = sum(item['price'] * item['quantity'] for item in cart.values())
        
        new_order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            table_number=request.session.get('table_number'),
            total_price=cart_total,
            status='Pending',
            is_paid=False # Payment is separate step / simulation
        )

        # 2. Create OrderItem objects
        order_items = []
        for item_id_str, item_data in cart.items():
            item_instance = Item.objects.filter(id=int(item_id_str)).first() # Link if it still exists
            order_items.append(OrderItem(
                order=new_order,
                item=item_instance,
                item_name=item_data['name'],
                item_price=item_data['price'],
                quantity=item_data['quantity']
            ))
        OrderItem.objects.bulk_create(order_items)
        
        # 3. Clear the cart
        del request.session['cart']
        
        # 4. Redirect to confirmation/billing (simulated)
        return render(request, 'myapp/checkout_success.html', {'order': new_order})
        
    return redirect('myapp:view_cart') # Should be handled by form POST

# --- Staff Dashboard/Reporting View (Point 3) ---

@staff_required
def staff_dashboard(request):
    """Dashboard for staff to view orders, revenue, and item sales."""
    
    # 1. Active Orders (Pending/Preparing)
    active_orders = Order.objects.filter(status__in=['Pending', 'Preparing']).order_by('-created_at')
    
    # 2. Key Metrics (Total Orders & Revenue)
    all_orders = Order.objects.all()
    total_orders_count = all_orders.count()
    total_revenue = all_orders.filter(is_paid=True).aggregate(total=Sum('total_price'))['total'] or 0.00
    
    # 3. Item Sales Report (How many specific item were sold)
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

# Placeholder for Order Status Update (Staff action)
@staff_required
def update_order_status(request, order_id, new_status):
    """Staff can update an order status (e.g., from Pending to Preparing)."""
    order = get_object_or_404(Order, id=order_id)
    if new_status in [choice[0] for choice in Order.STATUS_CHOICES]:
        order.status = new_status
        # Handle payment status here as part of billing integration
        if new_status == 'Completed':
            order.is_paid = True # Assuming completed means paid
        
        order.save()
    return redirect('myapp:staff_dashboard')