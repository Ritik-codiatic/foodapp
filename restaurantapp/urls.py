from django.urls import path
# local imp
from .views import HomeView,RestaurantView,ItemView
urlpatterns = [
    path('',HomeView.as_view()),
    path('<int:restaurant_id>/',RestaurantView.as_view()),
    path('<int:restaurant_id>/items/<int:category_id>',ItemView.as_view())
 ] 
