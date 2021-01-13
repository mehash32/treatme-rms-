from django import forms
from .models import UserAddress

class UserAddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = ["address", "address2", "city", "state", "country", "zipcode", "phone", "setDefault"]
