from django.urls import path
# local imp
from .views import HomeView, RestaurantView, ItemView, AddRestaurantView,RestaurantHome, AddMenuCategory, GetAddress, UpdateItem, AddItems, Search, AddCartView, CartView, EditRestaurant, ImageGallery, EditItemView

urlpatterns = [
    path('',HomeView.as_view()),
    path('<int:restaurant_id>/', RestaurantView.as_view()),
    path('items/<int:restaurant_id>/<int:category_id>', ItemView.as_view()),
    path('addrestaurant', AddRestaurantView.as_view()),
    path('restauranthome/<int:restaurant_id>', RestaurantHome.as_view(), name="restauranthome"),
    path('addmenucategory', AddMenuCategory.as_view()),
    path('getaddress', GetAddress.as_view()),
    path('restaurantitem/<int:restaurant_id>/<int:category_id>', UpdateItem.as_view()),
    path('additem/<int:restaurant_id>',AddItems.as_view(), name='additems'),
    path('search',Search.as_view(),name='search-result'),
   # path('addcart/<int:restaurant_id>/<int:item_id>',AddCartView.as_view()),
    path('addcart',AddCartView.as_view()),
    path('cart',CartView.as_view()),
    path('editrestaurant/<int:restaurant_id>',EditRestaurant.as_view()),
    path('image-gallery/<int:restaurant_id>',ImageGallery.as_view()),
    path('edit-item/<int:item_id>',EditItemView.as_view())
 ] 
