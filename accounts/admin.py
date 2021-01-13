from django.contrib import admin
from .models import UserStripe, UserAddress, UserDefaultAddress
# Register your models here.

admin.site.register(UserStripe)
admin.site.register(UserAddress)
admin.site.register(UserDefaultAddress)
