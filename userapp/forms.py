from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser
class UserForm(UserCreationForm):
    #confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "mobile_number",
                   "user_type", "address", "gender", "profile_pic", "city_name"]
    # def clean(self):
    #     cleaned_data = super(UserForm, self).clean()
    #     password = cleaned_data.get("password")
    #     confirm_password = cleaned_data.get("confirm_password")
        
    #     if password != confirm_password:
    #         raise forms.ValidationError(
    #             "password and confirm_password does not match"
    #         )
    

    # def clean_mobile_number(self):
    #     cleaned_data = super(UserForm, self).clean()
    #     mobile_number = cleaned_data.get("mobile_number")
    #     len_mobile = len(mobile_number)
    #     if len_mobile >= 11 or len_mobile <= 9:
    #         raise forms.ValidationError(
    #             "mobile number should contain 10 digits"
    #         )  

class LoginForm(ModelForm):
    class Meta:
        model = CustomUser  
        fields = ["email","password"]
    
    def clean(self) :
        pass

class UserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email','first_name','last_name','mobile_number','profile_pic','gender','address']