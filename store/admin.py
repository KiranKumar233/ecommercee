from django.contrib import admin
from .models import category,product,Cart,Order,OrderItem,profile

admin.site.register(category)
admin.site.register(product)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(profile)

