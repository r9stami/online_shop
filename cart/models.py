from django.db import models

from account.models import User
from product.models import Product, Color, Size


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='orders')
    total_price = models.PositiveIntegerField(default=0)
    is_paid = models.BooleanField(default=False)
    address = models.TextField(default='kos')

    def __str__(self):
        return f'{self.user}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)
    color = models.CharField(max_length=60)
    size = models.CharField(max_length=60)
    price = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product.title}'


class DiscountCode(models.Model):
    title = models.CharField(max_length=60)
    persentage = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}'


