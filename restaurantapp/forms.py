# local imp
from .models import *

# dajngo imp
from django.forms import ModelForm
from location_field.forms.plain import PlainLocationField

class RestaurantForm(ModelForm):
    location = PlainLocationField(based_fields=['city'],
                                  initial='22.826820400544058,75.87158203125001')
    class Meta:
        model = Restaurant
        exclude = ['owner']
        
class MenuCategoryForm(ModelForm):
    class Meta:
        model = MenuCategory
        fields = '__all__'

class ItemForm(ModelForm):
    class Meta:
        model = MenuItem
        fields = '__all__'

class ItemPriceForm(ModelForm):

    class Meta:
        model = Menu
        exclude = ['restaurant','item']