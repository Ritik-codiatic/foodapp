# local imp
from .models import *

# dajngo imp
from django.forms import ModelForm
from django import forms
# libs imp
from location_field.forms.plain import PlainLocationField

class RestaurantForm(ModelForm):
    location = PlainLocationField(based_fields=['city'],
                                  initial='22.826820400544058,75.87158203125001')
    class Meta:
        model = Restaurant
        exclude = ['owner']
        widgets = {
            'opening_time' : forms.TimeInput(attrs={'type': 'time'}),
            'closing_time' : forms.TimeInput(attrs={'type': 'time'})
        }
        
class MenuCategoryForm(ModelForm):
    class Meta:
        model = MenuCategory
        fields = '__all__'

class ItemForm(ModelForm):
    class Meta:
        model = MenuItem
        fields = '__all__'
        #exclude = ['menu_category']

class ItemPriceForm(ModelForm):

    class Meta:
        model = Menu
        exclude = ['restaurant','item']

class RestaurantImageForm(ModelForm):

    class Meta:
        model = RestaurantImage
        exclude = ['restaurant']