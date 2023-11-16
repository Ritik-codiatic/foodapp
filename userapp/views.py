from django.shortcuts import render,redirect
from django.contrib import auth,messages
from django.views.generic import View
from django.views.generic.list import ListView
from django.contrib.auth.forms import UserCreationForm

# local imp
from restaurantapp.models import *
from .forms import UserForm,LoginForm
from .models import *
# Create your views here.

class SignupFormView(View):
    '''view for signing up the user or owner'''

    form_class = UserForm
    template_name = 'user/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, self.template_name, context = {'form':form})


class LoginFormView(View):
    '''view to loging up the user or owner'''
    
    form_class = LoginForm
    template_name = 'user/login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, context = {'form':form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            user = auth.authenticate(
                email = form.cleaned_data["email"],
                password = form.cleaned_data["password"],
            )
            if user is not None:
                auth.login(request, user)
                if user.user_type == "Customer" :
                    return redirect('/') 
                else:
                    return redirect('/user/owner') 
            
        return render(request, self.template_name, context = {'form':form})
            
class LogOutView(View):
    '''view for log out'''
    def get(self, request, *args, **kwargs):
        auth.logout(request)
        return redirect('/')
    
# class OwnerView(View):
#     '''view to redirecting owner to owner page'''

#     template_name = 'owner/ownerhome.html'
#     def get(self, request, *args, **kwargs):
#         restaurant = Restaurant.objects.filter(owner__id=request.user.id)
#         return render(request, self.template_name, {'restaurants' : restaurant})
 

class UserProfileView(View):
    '''view for showing user profile'''

    template_name = 'user/user_profile.html'
    form_class = UserForm
    def get(self, request, *args, **kwargs):
        user = CustomUser.objects.get(id = request.user.id)
        user_form = self.form_class(instance=user)
        return render(request, self.template_name, context={'user_form':user_form})
    
    def post(self, request, *args, **kwargs):
        user_form = self.form_class(request.POST,request.FILES)
        if user_form.is_valid():
            user_form.save()
            return redirect('/')

def custom_page_not_found_view(request, exception):
    return render(request, "404.html", {})