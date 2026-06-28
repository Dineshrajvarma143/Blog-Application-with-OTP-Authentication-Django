from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import Blog
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
        model = Blog
        fields = ['title', 'content']


class ProfileForm(forms.ModelForm):
    password1 = forms.CharField(required=False, widget=forms.PasswordInput, label='New password')
    password2 = forms.CharField(required=False, widget=forms.PasswordInput, label='Confirm new password')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean(self):
        cleaned = super().clean()
        pw1 = cleaned.get('password1')
        pw2 = cleaned.get('password2')
        if pw1 or pw2:
            if pw1 != pw2:
                raise forms.ValidationError('Passwords do not match.')
            if len(pw1) < 8:
                raise forms.ValidationError('Password must be at least 8 characters.')
        return cleaned

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            # apply bootstrap-like class to all fields
            existing = field.widget.attrs.get('class', '')
            classes = (existing + ' form-input').strip()
            field.widget.attrs['class'] = classes