#dajngo imp
from django.urls import path

#local imp 

from .views import SignupFormView, LoginFormView, LogOutView, OwnerView

urlpatterns = [
    path('signup/', SignupFormView.as_view()),
    path('login/', LoginFormView.as_view()),
    path('logout/', LogOutView.as_view()),
    path('owner/', OwnerView.as_view()),
   
]