from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import DecimalField 

# Create your models here.
class Item(models.Model):
    
    def __str__(self):
        return self.item_name
    
    def get_absolute_url(self):
        return reverse('myapp:index')
    
    user_name = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    item_name = models.CharField(max_length=100)
    item_description = models.CharField(max_length=200)
    item_price = models.IntegerField()
    item_image = models.CharField(max_length=500, default="data:image/jpeg;base64,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")
    
    # NEW FIELD
    is_available = models.BooleanField(default=True)

    # NEW ORDERING MODELS
    # STATUS_CHOICES defined here so it is easily accessible by Order model.
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Preparing', 'Preparing'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    table_number = models.CharField(max_length=10, null=True, blank=True)
    # FIX: Reference the STATUS_CHOICES directly from the module level or by the class name (Order)
    status = models.CharField(max_length=10, choices=Item.STATUS_CHOICES, default='Pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} ({self.status})"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    item_name = models.CharField(max_length=100)
    item_price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def get_total(self):
        return self.item_price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.item_name}"