import stripe
from django.db import models
from django.conf import settings
from django.contrib.auth.signals import user_logged_in

# Create your models here.
class UserDefaultAddress(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shipping = models.ForeignKey('UserAddress', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} Address'


class UserAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=120)
    address2 = models.CharField(max_length=120, null=True, blank=True)
    city = models.CharField(max_length=120)

    state_choices = (
        ('Dhaka', 'Dhaka'),
        ('Khulna', 'Khulna'),
        ('Barishal', 'Barishal'),
    )

    state = models.CharField(max_length=120, choices=state_choices, null=True, blank=True)
    country = models.CharField(max_length=120)
    zipcode = models.CharField(max_length=25)
    phone = models.CharField(max_length=120)
    shipping = models.BooleanField(default=True)
    setDefault = models.BooleanField(verbose_name='Save address as default', default=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return f'{self.user.username} Address'

    def get_address(self):
        return "%s, %s, %s-%s, %s" %(self.address, self.city, self.state, self.zipcode, self.country)

    class Meta:
        ordering = ['-updated', '-timestamp']


class UserStripe(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=120)

    def __str__(self):
        return f'{self.stripe_id}'


stripe.api_key = settings.STRIPE_SECRET_KEY

def get_or_create_stripe(sender, user, *args, **kwargs):
    try:
        stripe_id = user.userstripe.stripe_id
    except UserStripe.DoesNotExist:
        customer = stripe.Customer.create(email = str(user.email))
        new_user_stripe = UserStripe.objects.create(user=user, stripe_id=customer.id)
    except:
        pass

user_logged_in.connect(get_or_create_stripe)
