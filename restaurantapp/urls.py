from django.urls import path
# local imp
from .views import HomeView, RestaurantView, ItemView, AddRestaurantView,RestaurantHome, AddMenuCategory, GetAddress, UpdateItem, AddItems

urlpatterns = [
    path('',HomeView.as_view()),
    path('<int:restaurant_id>/', RestaurantView.as_view()),
    path('<int:restaurant_id>/items/<int:category_id>', ItemView.as_view()),
    path('addrestaurant', AddRestaurantView.as_view()),
    path('restauranthome/<int:restaurant_id>', RestaurantHome.as_view(), name="restauranthome"),
    path('addmenucategory', AddMenuCategory.as_view()),
    path('getaddress', GetAddress.as_view()),
    path('restaurantitem/<int:restaurant_id>/<int:category_id>', UpdateItem.as_view()),
    path('additem/<int:restaurant_id>',AddItems.as_view())
 ] 
