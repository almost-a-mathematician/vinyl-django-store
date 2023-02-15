from django.contrib import admin
from .models import *

admin.site.register(Customer)
admin.site.register(Product)
class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','customer','date_ordered','complete']
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)
# admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
