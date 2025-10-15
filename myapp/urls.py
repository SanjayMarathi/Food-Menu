from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
    # Read/List View
    path('', views.index, name='index'), 
    # Detail View
    path('<int:id>/', views.detail, name='detail'), 
    # Create View
    path('add/', views.create_item, name='create_item'),
    # Update View
    path('update/<int:id>/', views.update_item, name='item_update'),
    # NEW: Delete View
    path('delete/<int:id>/', views.delete_item, name='item_delete'), 
]