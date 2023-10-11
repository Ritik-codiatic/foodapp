# django imp

from django.shortcuts import render,redirect
from django.contrib import auth,messages
from django.views.generic import View
from django.views.generic.list import ListView
# local imp

from .models import *
# Create your views here.

class HomeView(View):
    '''view for rendering main page'''

    template_name = 'user/home.html'
    model = Restaurant.objects.all()
    def get(self, request, *args, **kwargs):
      return render(request, self.template_name, {'restaurant_list':self.model})
    
class RestaurantView(View):
    '''view for showing restaurant menu category and its detail'''

    template_name = 'restaurant/main.html'

    def get(self, request, *args, **kwargs):
        restaurant_id = kwargs['restaurant_id']
        restaurant = Restaurant.objects.get(id=restaurant_id)
        list1 = []
        for item in restaurant.menu_set.all():
            list1.append(item.item.menu_category)
        menu_category = []
        for i in list1:
            if i not in menu_category:
                menu_category.append(i)
        return render(request, self.template_name, context = {'restaurant':restaurant,'menu_category':menu_category})
    
class ItemView(View):
    '''view to display menu items of a category'''

    template_name = 'restaurant/item.html'

    def get(self, request, *args, **kwargs):
        category_id = kwargs['category_id']
        restaurant_id = kwargs['restaurant_id']
        menucategory = MenuCategory.objects.get(id = category_id)
        restaurant = Restaurant.objects.get(id = restaurant_id)
        #print(restaurant.menu_set.all()[0].item.menu_category.id)
        items = []
        for item in restaurant.menu_set.all():
            if item.item.menu_category.id == menucategory.id:
                items.append(item.item)
        #items = menucategory.menuitem_set.all()
        return render(request, self.template_name, context = {'items':items,'menucategory':menucategory})