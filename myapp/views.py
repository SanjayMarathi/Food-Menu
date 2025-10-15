from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Item
from .forms import ItemForm

# Menu List View (Index)
def index(request):
    item_list = Item.objects.all()
    context = {
        'item_list':item_list
    }
    return render(request,"myapp/index.html",context)

# Item Detail View
def detail(request, id):
    item = Item.objects.get(id = id)
    return render(request, 'myapp/detail.html', {
        'item':item
    })
      
# Create Item View
def create_item(request):
    form = ItemForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('myapp:index')
        
    context = {
        'form':form,
        'title': 'Add New Food Item' # Context for form title
    }
    return render(request, 'myapp/item_form.html', context)

# Update Item View
def update_item(request, id):
    item = Item.objects.get(id = id)
    form = ItemForm(request.POST or None, instance = item)
    if request.method == 'POST': 
        if form.is_valid():
            form.save()
            return redirect('myapp:detail', id=item.id) # Redirect to detail after update
            
    context = {
        'form':form,
        'item': item, # Pass item instance for potential use in template
        'title': f'Update {item.item_name}' # Context for form title
    }
    return render(request, 'myapp/item_form.html', context)

# NEW: Delete Item View
def delete_item(request, id): 
    item = Item.objects.get(id = id)
    if request.method == 'POST':
        item.delete()
        return redirect('myapp:index') # Redirect to menu list after deletion
        
    context = {
        'item': item
    }
    return render(request, 'myapp/item_delete.html', context)