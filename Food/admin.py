from django.contrib import admin
from .models import foodItem, restaurantList, UserProfile, Wishlist, Rating, Cart, CartItem, Manager, Order

# Register your models here.
admin.site.register(foodItem)
admin.site.register(restaurantList)
admin.site.register(UserProfile)
admin.site.register(Wishlist)
admin.site.register(Rating)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Manager)
admin.site.register(Order)
