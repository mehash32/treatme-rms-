from django import forms
from stuffs.models import foodItem, restaurantList, Comment

class ItemForm(forms.ModelForm):
    class Meta:
        model = foodItem
        fields = ('Item_name', 'Image', 'Description', 'Price', 'Availability', 'onTrend')


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = restaurantList
        fields = ('Restaurant_name', 'Cover_Photo', 'Logo', 'Bio', 'Description', 'Food_type', 'Opens', 'Location', 'Contact_number')


class RestaurantUpdateForm(forms.ModelForm):
    class Meta:
        model = restaurantList
        fields = ('Restaurant_name', 'Cover_Photo', 'Logo', 'Bio', 'Description', 'Food_type', 'Opens', 'Location', 'Contact_number')
