from django.urls import path
# local imp
from .views import HomeView, RestaurantView, ItemView, AddRestaurantView, RestaurantHome, AddMenuCategory
urlpatterns = [
    path('',HomeView.as_view()),
    path('<int:restaurant_id>/',RestaurantView.as_view()),
    path('<int:restaurant_id>/items/<int:category_id>',ItemView.as_view()),
    path('addrestaurant',AddRestaurantView.as_view()),
    path('<int:restaurant_id>/restauranthome',RestaurantHome.as_view()),
    path('addmenucategory',AddMenuCategory.as_view()),
 ] 
