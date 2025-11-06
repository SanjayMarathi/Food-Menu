from django.contrib import admin
from .models import Item, Order, OrderItem

# Register your models here.

# Inline for OrderItems in the Order Admin
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('item_name', 'item_price', 'quantity')
    can_delete = False

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'table_number', 'status', 'total_price', 'is_paid', 'created_at')
    list_filter = ('status', 'is_paid', 'created_at')
    search_fields = ('user__username', 'table_number')
    inlines = [OrderItemInline]
    readonly_fields = ('user', 'table_number', 'total_price', 'created_at', 'updated_at')
    
admin.site.register(Item)
# We can also register OrderItem if needed, but it's handled via OrderAdmin now