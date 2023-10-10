from django.urls import path
# local imp
from .views import HomeView,RestaurantView
urlpatterns = [
    path('',HomeView.as_view()),
    path('<int:restaurant_id>/',RestaurantView.as_view())
 ] 
