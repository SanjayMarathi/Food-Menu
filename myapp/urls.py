from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
    # --- Staff Management Views ---
    path('management/', views.index, name='index'), 
    path('management/detail/<int:id>/', views.detail, name='detail'), 
    path('management/add/', views.create_item, name='create_item'),
    path('management/update/<int:id>/', views.update_item, name='item_update'),
    path('management/delete/<int:id>/', views.delete_item, name='item_delete'), 
    path('management/dashboard/', views.staff_dashboard, name='staff_dashboard'), 
    path('management/order/<int:order_id>/status/<str:new_status>/', views.update_order_status, name='update_order_status'),
    # NEW QR CODE ROUTE
    path('management/qr/<str:table_id>/', views.generate_qr_code, name='generate_qr_code'),

    # --- Customer Facing Views ---
    path('', views.menu, name='menu'), # Public-facing Menu
    path('table/<str:table_id>/', views.menu, name='menu_with_table'), # QR Code Landing Spot
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/success/', views.checkout, name='checkout_success'), 
]