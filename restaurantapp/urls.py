from django.urls import path
# local imp
from .views import *

urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('<int:restaurant_id>/', RestaurantView.as_view()),
    path('items/<int:restaurant_id>/<int:category_id>', ItemView.as_view()),
    path('addrestaurant', AddRestaurantView.as_view()),
    path('restauranthome/<int:restaurant_id>', RestaurantHome.as_view(), name="restauranthome"),
    path('addmenucategory', AddMenuCategory.as_view()),
    path('getaddress', GetAddress.as_view()),
    path('additem/<int:restaurant_id>',AddItems.as_view(), name='additems'),
    path('search',Search.as_view(),name='search-result'),
    path('addcart',AddCartView.as_view()),
    path('editrestaurant/<int:restaurant_id>',EditRestaurant.as_view()),
    path('image-gallery/<int:restaurant_id>',ImageGallery.as_view()),
    path('edit-item/<int:item_id>',EditItemView.as_view()),
    path('success/', PaymentSuccessView.as_view(), name='success'),
    path('failed/', PaymentFailedView.as_view(), name='failed'),
    path('history/', OrderHistoryListView.as_view(), name='history'),
    path('api/checkout-session/<int:id>/', create_checkout_session, name='api_checkout_session'),
    path('order', OrderHistoryListView.as_view(), name="orders"),
    path('feedback/<int:restaurant_id>/<int:order_id>',RatingReviewView.as_view(),name='feedback'),
 ] 
