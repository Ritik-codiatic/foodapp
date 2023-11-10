# django imp
from typing import Any
from django.db.models.query import QuerySet
from django.http.response import HttpResponseNotFound, JsonResponse, HttpResponse
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
from django.core.mail import send_mail,EmailMultiAlternatives
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
    
    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous or request.user.user_type == "Customer":
            model = Restaurant.objects.all().order_by('id')   
        else:
            model = Restaurant.objects.filter(owner = request.user).all().order_by('id')

        if request.GET.get('search'):
            restaurant = request.GET.get('search', '').strip()
            model = Restaurant.objects.filter(Q(name__icontains=restaurant) | Q(address__icontains=restaurant)).all().order_by('id')

        if request.GET.get('rating'):
            rating = request.GET.get('rating')
            
            # model = RestaurantRating.objects.filter(restaurant=4).aggregate(Avg("rating"))["rating__avg"]
            model = Restaurant.objects.all().annotate(rating_avg=Avg('restaurantrating__rating')).filter(rating_avg__gte=rating).order_by('id')
            # model = []
            # for restaurant in restaurants:
            #     if restaurant.rating_avg >= int(rating):
            #         model.append(restaurant)
            
        p = Paginator(model, 9)
        page_number = request.GET.get('page')
        try:
            page_obj = p.get_page(page_number)
        except PageNotAnInteger:
            page_obj = p.page(1)
        except EmptyPage:
            page_obj = p.page(p.num_pages)
    
        return render(request, self.template_name, {'page_obj':page_obj})
    
from location_field.forms.plain import PlainLocationField
class RestaurantView(View):
    '''view for showing restaurant menu category and its detail'''

    template_name = 'restaurant/main.html'

    def get(self, request, *args, **kwargs):
        restaurant_id = kwargs['restaurant_id']
        restaurant = Restaurant.objects.get(id=restaurant_id)
        location = PlainLocationField(based_fields=['city'],
                                  initial=restaurant.location)
        
        menu = Menu.objects.filter(restaurant__id = restaurant_id)
        # not optimized
        list1 = []
        for item in restaurant.menu_set.all():
            list1.append(item.item.menu_category)
        menu_category = []
        for i in list1:
            if i not in menu_category:
                menu_category.append(i)
        return render(request, self.template_name, context = {'restaurant':restaurant,'menu_category':menu_category,'location':location})
    
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
        breakpoint()
        if itemform.is_valid() and itempriceform.is_valid():
            itempriceform.save()
            # itemform.save()
            breakpoint()
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    
    def delete(self, request, *args, **kwargs):
        item_id = kwargs['item_id']
        Menu.objects.get(id = item_id).delete()
        return JsonResponse({})
    

class AddRestaurantView(View):
    '''view to add restaurant'''
    
    template_name = 'add_restaurant.html'
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
            return redirect('/')
        
    
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
        
        if request.GET.get('location'):
            location = request.GET.get('location')
            coordinates = location.split(',')
            geolocator = Nominatim(user_agent="geoapiExercises")
            address = geolocator.reverse(coordinates[0]+","+coordinates[1])
            address = address[0]
        else:
            
            lat = request.GET.get('latitude')
            lng = request.GET.get('longitude')
            geolocator = Nominatim(user_agent="geoapiExercises")
            address = geolocator.reverse(str(lat)+","+str(lng))
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
            return redirect(reverse('main_page',kwargs= {'restaurant_id':restaurant_id}))
    

class AddCartView(View):
    '''view for adding item to cart '''

    template_name = 'restaurant/cart.html'
    def get(self, request, *args, **kwargs):
        cart ,_= Cart.objects.get_or_create(user=request.user,is_paid = False)
        cart_items = CartItem.objects.filter(cart=cart).order_by('cart_item__item__name')
        stripe_publishable_key = settings.STRIPE_PUBLISHABLE_KEY
      #  total_price = cart_items.aggregate(total = Sum('cart_item__price'))
        return render(request, self.template_name, {'cart_item':cart_items,'stripe_publishable_key':stripe_publishable_key})
                                                    #'total_price':total_price['total']})

    def post(self, request, *args, **kwargs):
        item_id = request.POST.get('item_id')
        item_quantity = request.POST.get('quantity') 
        item = Menu.objects.get(id = item_id)
        cart ,_= Cart.objects.get_or_create(user = request.user,is_paid = False)
        cart.save()
        cartitem ,_= CartItem.objects.get_or_create(cart_item=item, cart=cart)
        cartitem.quantity = item_quantity
        cartitem.save()

        return JsonResponse({'item_quantity':item_quantity})
    
    def delete(self, request, *args, **kwargs):
        delete = QueryDict(request.body)
        item_id = delete.get('remove_item_id')
        item = Menu.objects.get(id = item_id)
        cart = Cart.objects.get(user = request.user,is_paid= False)
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
            return redirect(reverse('main_page', kwargs={'restaurant_id':restaurant_id}))
    
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

    request_data = json.loads(request.body)
    cart = get_object_or_404(Cart, pk=id)
    total_price = request_data['grand_total']
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        # Customer Email is optional,
        # It is not safe to accept email directly from the client side
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                    'name': cart.user.email,
                    },
                    'unit_amount': int(total_price*100),
                },
                'quantity': 1,
            }
        ],
        metadata={'user':request.user.first_name,
                       'cart':cart,
                       'amount':int(total_price*100)},
        mode='payment',
        success_url=request.build_absolute_uri(
            reverse('success')
        ) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse('failed')),
    )
    order = OrderDetail()
    order.user = request.user
    order.cart = cart
    order.stripe_payment_intent = checkout_session.id
    order.amount = total_price
    order.save()

    # return JsonResponse({'data': checkout_session})
    return JsonResponse({'sessionId': checkout_session.id})


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
     
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
       
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        print("Payment was successful.")
        session_id = event['data']['object']['id']
        # print(event['data']['object']['metadata'])
        order = get_object_or_404(OrderDetail, stripe_payment_intent=session_id)
        order.has_paid = True
        order.save()
        cart = order.cart
        cart.is_paid = True
        cart.save()
        subject = 'thanks for ordering from FoodTresure'
        message = f'Hi , Please review your order from this link /payments/order_history.html . your order no. is  '
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['ritik.makwan@codiatic.com', ]
        html_content = render_to_string(
        'user/email.html'
        )
        msg = EmailMultiAlternatives( subject, html_content, email_from, recipient_list )
        # msg.attach_alternative(html_content,'orders/html')
        msg.content_subtype = 'html'
        msg.send()

    return HttpResponse(status=200)

from django.template.loader import render_to_string
class PaymentSuccessView(TemplateView):
    template_name = "payments/payment_success.html"

    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        if session_id is None:
            return HttpResponseNotFound()
        
        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.retrieve(session_id)

        # order = get_object_or_404(OrderDetail, stripe_payment_intent=session_id)
        # order.has_paid = True
        # order.save()
        # cart = order.cart
        # cart.is_paid = True
        # cart.save()
        
        return render(request, self.template_name)
    
class PaymentFailedView(TemplateView):
    template_name = "payments/payment_failed.html"

class OrderHistoryListView(ListView):
    '''view for showing user order history'''

    context_object_name = 'order_list'
    template_name = 'payments/order_history.html'

    def get_queryset(self):
        return OrderDetail.objects.filter(user = self.request.user)
    
    def get_context_data(self, **kwargs: Any):

        return super().get_context_data(**kwargs)
    
class RatingReviewView(View):
    '''view for rating restaurant'''

    template_name = 'restaurant/feedback.html'
    def get(self, request, *args, **kwargs):
        restaurant_id = kwargs['restaurant_id']
        order_id = kwargs['order_id']
        restaurant = Restaurant.objects.get(id = restaurant_id)
        order = OrderDetail.objects.get(id = order_id)
        return render(request, self.template_name, context={'restaurant':restaurant, 'order':order})

    def post(self, request, *args, **kwargs):
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        order_id = kwargs['order_id']
        restaurant_id = kwargs['restaurant_id']
        restaurant = Restaurant.objects.get(id = restaurant_id)
        order = OrderDetail.objects.get(id = order_id)
        RestaurantRating.objects.create(
            user = request.user,
            restaurant = restaurant,
            order = order,
            rating = rating,
            comment = comment)
        return JsonResponse({})

class RestaurantOrderView(View):
    '''view for showing orders to restaurant'''

    template_name = 'owner/restaurant_orders.html'
    # context_object_name = 'order_list'
    # model = OrderDetail

    # def get_context_data(self, **kwargs: Any):
    #     context = super().get_context_data(**kwargs)
    #     restaurant_id = self.kwargs['restaurant_id']
    #     context['restaurant'] = Restaurant.objects.get(id = restaurant_id)
    #     return context
    

    def get(self, request, *args, **kwargs):
        restaurant_id = kwargs['restaurant_id']
        restaurant = Restaurant.objects.get(id = restaurant_id)
        menu_ids = restaurant.menu_set.values_list('id', flat=True)
        cart_items = CartItem.objects.filter(cart_item_id__in=menu_ids)#,cart_item__restaurant_id=restaurant_id)
        carts = [cart_item.cart.id for cart_item in cart_items]
        orders = OrderDetail.objects.filter(cart_id__in=carts)#.annotate(items='cart__cart_item').filter(items__restaurant__id=restaurant_id)
        return render(request, self.template_name , context={'restaurant':restaurant, 'order_list':orders,'cart_items':cart_items})

# class RatingReviewView(DetailView):
#     '''view for rating of a restaurant'''

#     template_name = 'restaurant/feedback.html'
#     model = Menu
#     context_object_name = 'menu_item'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     rating = self.request.GET.get['']
    #     context['rating'] = None
    #     return 
