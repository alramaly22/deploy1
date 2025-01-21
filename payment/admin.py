from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem

# Create an OrderItem Inline
class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0
    fields = ['product', 'quantity', 'price', 'size']  # إضافة حقل size

# Extend our Order Model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ["date_ordered"]
    fields = ["user", "full_name", "email", "shipping_address", "amount_paid", "date_ordered", "shipped", "date_shipped"]
    inlines = [OrderItemInline]

# Register models
admin.site.register(ShippingAddress)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)