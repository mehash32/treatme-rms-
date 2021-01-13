from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class restaurantList(models.Model):
    Restaurant_name = models.CharField(max_length=100)
    Cover_Photo = models.ImageField(default='default_Restaurant.jpg', blank='True', upload_to='res_pics')
    Logo = models.ImageField(default='default-logo.png', blank='True', upload_to='res_pics')
    Bio = models.CharField(max_length=150, null=True, blank=True)
    Description = models.TextField(default="", blank=True)
    Food_type = models.CharField(max_length=100, null=True, blank=True)
    Opens = models.TextField(blank=True)
    Location = models.TextField(default="", blank=True)
    Contact_number = models.CharField(max_length=100, default="", blank=True)
    is_valid = models.BooleanField(default=False)

    def __str__(self):
        if self.is_valid:
            return f'Verified : {self.Restaurant_name}'
        else:
            return f'Unverified : {self.Restaurant_name}'

    def ratings(self):
        rates = Review.objects.filter(rest=self)
        count = 0
        total = 0

        for r in rates:
            total = total + r.stars
            count = count + 1

        if count == 0:
            return False
        else:
            avg = float(total/count)
            return "%.1f/5.0" %(avg)


    def review_count(self):
        return Review.objects.filter(rest=self).count()


class foodItem(models.Model):
    Restaurant_name = models.ForeignKey(restaurantList, on_delete=models.CASCADE, null=True)
    Item_name = models.CharField(max_length=100)
    Image = models.ImageField(default='default_Food.jpg', blank='True', upload_to='pics')
    Description = models.TextField(null=True, blank=True)
    Price = models.DecimalField(max_digits=100, decimal_places=2)

    choices = (
        ('Available', 'Available'),
        ('Out of Stock', 'Out of Stock'),
    )

    Availability = models.CharField(max_length=15, default='Available', choices=choices)
    onTrend = models.BooleanField(default=False)
    

    def __str__(self):
        return f'{self.Restaurant_name} : {self.Item_name}'

    def get_average_ratings(self):
        rates = Rating.objects.filter(item=self)
        
        count = 0
        total = 0

        for r in rates:
            total = total + r.stars
            count = count + 1

        if count == 0:
            return False
        else:
            avg = float(total/count)
            return "%.1f/5.0 (%d)" %(avg, count)

    def comment_count(self):
        return Comment.objects.filter(item=self).count()

    class Meta:
        ordering = ['Item_name']


class Rating(models.Model):
    item = models.ForeignKey(foodItem, related_name='rate', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stars = models.IntegerField(default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ]
    )
    rated = models.IntegerField(default=0)


    def __str__(self):
        return f'Ratings for {self.item.Item_name}'


class Comment(models.Model):
    item = models.ForeignKey(foodItem,related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    text = models.TextField() 

    def __str__(self):
        return f'{self.user.username} Comment On {self.item.Item_name}'


class Review(models.Model):
    rest = models.ForeignKey(restaurantList, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    date_added = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    stars = models.IntegerField(default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ]
    )

    def __str__(self):
        return f'{self.user.username} Review On {self.rest.Restaurant_name}'


class Voucher(models.Model):
    card_id = models.CharField(default="#abc123", max_length=8)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    validity = models.CharField(default="2 Months", max_length=120)
