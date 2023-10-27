# django imp
from django.http.response import HttpResponseNotFound, JsonResponse
from django.urls import reverse, reverse_lazy
from .models import *
from django.views.generic import ListView, CreateView, DetailView, TemplateView
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import auth,messages
from django.views.generic import View
from django.http import JsonResponse,HttpResponseRedirect,QueryDict
from django.urls import reverse
from django.db.models import Q,Subquery
# local imp

from .models import *
from .forms import *

# lib imp
from geopy.geocoders import Nominatim
import stripe
import json
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
        items = Menu.objects.filter(restaurant=restaurant,item__menu_category = menucategory)
        # .annotate(quantity=Subquery(
        # CartItem.objects.filter(
        #     cart_item__restaurant=restaurant,cart_item__item__menu_category=menucategory)))
        return render(request, self.template_name, context = {'items':items,'menucategory':menucategory,'restaurant':restaurant})

class EditItemView(View):
    '''view to edit restaurant item'''

    template_name = 'edit_item.html'  
    itemform_class = ItemForm
    itempriceform_class = ItemPriceForm
    def get(self, request, *args, **kwargs):
        item_id = kwargs['item_id']
        menu = Menu.objects.get(id = item_id)
        itempriceform = self.itempriceform_class(instance=menu)
        menuitem = MenuItem.objects.get(id = menu.item.id)
        itemform = self.itemform_class(instance=menuitem)
        return render(request, self.template_name, context={'itemform':itemform,'itempriceform':itempriceform})
    
    def post(self, request, *args, **kwargs):
        itempriceform = self.itempriceform_class(request.POST,request.FILES)
        itemform = self.itemform_class(request.POST)
        if itemform.is_valid() and itempriceform.is_valid():
            itempriceform.save()
            itemform.save()
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    
    def delete(self, request, *args, **kwargs):
        item_id = kwargs['item_id']
        Menu.objects.get(id = item_id).delete()
        return JsonResponse({})
    

class AddRestaurantView(View):
    '''view to add restaurant'''
    
    template_name = 'addrestaurant.html'
    form_class = RestaurantForm
    def get(self, request, *args, **kwargs):
        restaurantform = self.form_class()
        return render(request, self.template_name, context = {'restaurantform':restaurantform })
    
    def post(self, request, *args, **kwargs):
        restaurantform = self.form_class(request.POST)
        if restaurantform.is_valid():
            owner = CustomUser.objects.get(id = request.user.id)
            restaurantform.instance.owner = owner
            restaurantform.save()
            return redirect('/user/owner')
        
    
class RestaurantHome(View):
    '''view to show restaurant categories to owner'''

    form_class = MenuCategoryForm
    template_name = 'restauranthome.html'
    def get(self, request, *args, **kwargs):
        restaurant_id = kwargs['restaurant_id']
        categoryform = self.form_class()
        restaurant = Restaurant.objects.get(id = restaurant_id)
        list1 = []
        for item in restaurant.menu_set.all():
            list1.append(item.item.menu_category)
        menucategory = []
        for item in list1:
            if item not in menucategory:
                menucategory.append(item)
        return render(request, self.template_name, context={'categoryform':categoryform,'menucategory':menucategory,'restaurant':restaurant})


class AddMenuCategory(View):
    '''view to add menu category'''

    form_class = MenuCategoryForm
    template_name = 'addmenucategory.html'
    def get(self, request, *args, **kwargs):
        categoryform = self.form_class()
        return render(request, self.template_name, context={'categoryform':categoryform})

class GetAddress(View):
    def get(self, request, *args, **kwargs):
        location = request.GET.get('location')
        coordinates = location.split(',')
        geolocator = Nominatim(user_agent="geoapiExercises")
        address = geolocator.reverse(coordinates[0]+","+coordinates[1])
        address = address[0]
        
        return JsonResponse({'address':address})
    
    
class AddItems(View):
    '''add items by owner'''
    
    template_name = 'additem.html'
    itemform_form_class = ItemForm
    itemprice_form_class = ItemPriceForm
    def get(self, request, *args, **kwargs):
        itemform = self.itemform_form_class()
        itempriceform = self.itemprice_form_class()
        return render(request, self.template_name, context={'itemform':itemform, 'itempriceform':itempriceform})

    def post(self, request, *args, **kwargs):
        restaurant_id = kwargs['restaurant_id']
        restaurant = Restaurant.objects.get(id=restaurant_id)
        itemform = self.itemform_form_class(request.POST)
        itempriceform = self.itemprice_form_class(request.POST,request.FILES)
        if itemform.is_valid() and itempriceform.is_valid():
            item = itemform.save()
            itempriceform.instance.restaurant = restaurant
            itempriceform.instance.item = item
            itempriceform.save()
            return redirect(reverse('restauranthome',kwargs= {'restaurant_id':restaurant_id}))
    
class Search(View):
    '''view for searching restaurant'''

    template_name = 'user/home.html'
    def get(self, request, *args, **kwargs):
        restaurant = request.GET.get('search', '').strip()
        result_restaurant = Restaurant.objects.filter(Q(name__icontains=restaurant) | Q(address__icontains=restaurant))
        return render(request, self.template_name, {'restaurant_list':result_restaurant})
    

class AddCartView(View):
    '''view for adding item to cart '''

    template_name = 'restaurant/cart.html'
    def get(self, request, *args, **kwargs):
        cart ,_= Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart.id).order_by('cart_item__item__name')
      #  total_price = cart_items.aggregate(total = Sum('cart_item__price'))
        return render(request, self.template_name, {'cart_item':cart_items})
                                                    #'total_price':total_price['total']})

    def post(self, request, *args, **kwargs):
        item_id = request.POST.get('item_id')
        item_quantity = request.POST.get('quantity') 
        item = Menu.objects.get(id = item_id)
        cart ,_= Cart.objects.get_or_create(user = request.user)
        cart.save()
        cartitem ,_= CartItem.objects.get_or_create(cart_item=item, cart=cart)
        cartitem.quantity = item_quantity
        cartitem.save()

        return JsonResponse({'item_quantity':item_quantity})
    
    def delete(self, request, *args, **kwargs):
        delete = QueryDict(request.body)
        item_id = delete.get('remove_item_id')
        item = Menu.objects.get(id = item_id)
        cart = Cart.objects.get(user = request.user)
        cartitem = CartItem.objects.get(cart_item=item, cart=cart).delete()
        return JsonResponse({})
    
class EditRestaurant(View):
    '''view for editing restaurant'''

    form_class = RestaurantForm
    template_name = 'restaurantprofile.html'
    def get(self, request, *args, **kwargs):
        restaurant_id = kwargs['restaurant_id']
        restaurant = Restaurant.objects.get(id = restaurant_id)
        form = self.form_class(instance=restaurant)

        return render(request, self.template_name, {'form':form})
    
    def post(self, request, *args, **kwargs):
        restaurant_id = kwargs['restaurant_id']
        owner = CustomUser.objects.get(id = request.user.id)
        form = self.form_class(request.POST)
        if form.is_valid():
            form.instance.id = restaurant_id
            form.instance.owner = owner
            form.save()
            return redirect(reverse('restauranthome', kwargs={'restaurant_id':restaurant_id}))
    
    def delete(self, request, *args, **kwargs):
        restaurant_id = kwargs['restaurant_id']
        Restaurant.objects.get(id = restaurant_id).delete()
        return JsonResponse({})

class ImageGallery(View):
    '''view for viewing image'''

    form_class = RestaurantImageForm
    template_name = 'image_gallery.html'
    def get(self, request, *args, **kwargs):
        image_form = self.form_class()
        restaurant_id = kwargs['restaurant_id']
        images = RestaurantImage.objects.filter(restaurant=restaurant_id)
        return render(request, self.template_name, context={'images':images,'image_form':image_form})
    
    def post(self, request, *args, **kwargs):
        restaurant_id = kwargs['restaurant_id']
        imageform = RestaurantImageForm(request.POST,request.FILES)
        restaurant = Restaurant.objects.get(id = restaurant_id)
        if imageform.is_valid():
            imageform.instance.restaurant = restaurant
            imageform.save()
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        
    def delete(self, request, restaurant_id, *args, **kwargs):
        RestaurantImage.objects.get(id = restaurant_id).delete()
        return JsonResponse({})
    
@csrf_exempt
def create_checkout_session(request, id):
	pass


class PaymentSuccessView(TemplateView):
    pass

class PaymentFailedView(TemplateView):
    pass

class OrderHistoryListView(ListView):
    pass