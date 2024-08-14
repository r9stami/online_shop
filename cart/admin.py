from django.contrib import admin
from .models import Order , OrderItem , DiscountCode


class OrderItemInline(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('total_price','is_paid')
    list_filter = ('is_paid',)
    inlines = [OrderItemInline]


admin.site.register(DiscountCode)
