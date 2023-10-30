#dajngo imp
from django.urls import path
from django.contrib.auth import views
from django.views.generic import TemplateView
#local imp 

from .views import SignupFormView, LoginFormView, LogOutView, OwnerView, UserProfileView

urlpatterns = [
    path('user-profile',UserProfileView.as_view()),
    path('signup/', SignupFormView.as_view()),
   # path('login/', LoginFormView.as_view()),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', LogOutView.as_view()),
    path('owner/', OwnerView.as_view()),
    path('password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password-change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]