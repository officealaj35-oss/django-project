from django.contrib import admin
from .models import Product, Contact, Orders, OrderUpdate

class OrderUpdateAdmin(admin.ModelAdmin):
    list_display = ('update_id', 'order', 'update_desc', 'timestamp')
    search_fields = ('order__order_id', 'update_desc')
    list_filter = ('timestamp',)

admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(Orders)
admin.site.register(OrderUpdate, OrderUpdateAdmin)