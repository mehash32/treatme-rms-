from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from stuffs.models import foodItem, restaurantList, Rating
from django.conf import settings
from accounts.models import UserAddress, UserDefaultAddress
from PIL import Image

User = get_user_model()

# Create your models here.
class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Restaurant = models.OneToOneField(restaurantList, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.Restaurant.Restaurant_name} : {self.user.username}'


class Profile(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   is_manager = models.BooleanField(verbose_name="is_manager", default=False)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Profile_picture = models.ImageField(default='default.jpg', upload_to='profile_pics')
    Phone_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.Profile_picture.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.Profile_picture.path)


class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    wished_item = models.ForeignKey(foodItem, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} : {self.wished_item.Item_name}'


class Cart(models.Model):
    restaurant = models.ForeignKey(restaurantList, on_delete=models.CASCADE, null=True, blank=True)
    sub_total = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    tax_total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    final_total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'Cart : {self.id}'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, null=True, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(foodItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    comment = models.CharField(max_length=120, null=True, blank=True)
    line_total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        try:
            return f'Cart Id : {self.cart.id}'
        except:
            return self.product.Item_name


class Order(models.Model):
    STATUS_CHOICES = (
        ("Started", "Started"),
        ("Abandoned", "Abandoned"),
        ("Finished", "Finished")
    )

    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=120, default='ABCDEF', unique=True)
    transaction_id = models.CharField(max_length=120, default='ABCDEFGHIJKL')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(restaurantList, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=120, choices=STATUS_CHOICES)
    address = models.OneToOneField(UserAddress, on_delete=models.CASCADE, blank=True, null=True)
    sub_total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    tax_total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    final_total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    charged = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    viewed = models.BooleanField(default=False)
