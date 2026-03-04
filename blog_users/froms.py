from django import forms
from .models import Bloguser,Create_blog
class Registerform(forms.ModelForm):
    class Meta:
        model = Bloguser
        fields = ['full_name','age','phone','registered_email']

class Loginform(forms.Form):
    full_name = forms.CharField(max_length=100)
    registered_email = forms.EmailField()

class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6)

class Createform(forms.ModelForm):
    class Meta:
        model = Create_blog
        fields = ['user','title','content','penname']