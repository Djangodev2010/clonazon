from django import forms
from django.contrib.auth.models import User
from . models import Product, Review, CartItem
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    avatar = forms.ImageField(label='Profile Picture:')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")

        return password1

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Invalid login credentials")
        return cleaned_data


class RatingForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['stars', 'review_text']
        widgets = {
            'stars': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]),
        }

class CartForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']

        
