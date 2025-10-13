from django.shortcuts import render
from django.http import HttpResponse
from .models import Item
# Create your views here.
def index(request):
    item_list = Item.objects.all()
    context = {
        'item_list':item_list
    }
    return render(request,"myapp/index.html",context)

def detail(request, id):
    item = Item.objects.get(id = id)
    return render(request, 'myapp/detail.html', {
        'item':item
    })
      
    
def item(reques):
    return HttpResponse("<h1>This is an item view.</h1>")