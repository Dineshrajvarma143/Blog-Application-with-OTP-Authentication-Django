from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import Bloguser,Create_blog
from django.contrib.auth.models import User

class Registerform(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class Loginform(AuthenticationForm):
    pass


class Createform(forms.ModelForm):
    class Meta:
        model = Create_blog
        fields = ['title','content','penname']