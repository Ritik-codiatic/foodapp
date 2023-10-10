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
    '''view for showing restaurant menu and its detail'''

    template_name = 'restaurant/main.html'

    def get(self, request, *args, **kwargs):
       restaurant_id = kwargs['restaurant_id']
       menu = Menu.objects.filter(restaurant__id=restaurant_id)
       restaurant = Restaurant.objects.get(id=restaurant_id)
       return render(request, self.template_name, {'restaurant':restaurant,'menu':menu})