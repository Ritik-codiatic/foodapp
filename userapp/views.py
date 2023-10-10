from django.shortcuts import render,redirect
from django.contrib import auth,messages
from django.views.generic import View
from django.views.generic.list import ListView
# local imp

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
            return redirect('/')
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
            
        messages.info(request, "!login failed")
        return render(request, self.template_name, context = {'form':form})
            
class LogOutView(View):
    '''view for log out'''
    def get(self, request, *args, **kwargs):
        auth.logout(request)
        return redirect('/')
    
class OwnerView(View):
    '''view to redirecting owner to owner page'''
    template_name = 'owner/ownerhome.html'
    def get(self, request, *args, **kwargs):
        return render(request,self.template_name)
 
