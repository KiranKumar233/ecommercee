from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from .models import User, Review, Reply, ContactMessage
from django import forms

class CustomerUserForm(UserCreationForm):
    username = forms.CharField(widget = forms.TextInput(attrs = {'class':'form-control my-2', 'placeholder':'Enter Username'}))
    email = forms.CharField(widget = forms.TextInput(attrs = {'class':'form-control my-2', 'placeholder':'Enter Email'}))
    password1 = forms.CharField(widget = forms.TextInput(attrs = {'class':'form-control my-2', 'placeholder':'Enter Password', 'type':'password'}))
    password2 = forms.CharField(widget = forms.TextInput(attrs = {'class':'form-control my-2', 'placeholder':'Enter Confirm Password', 'type':'password'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content']

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label="Email", max_length=254, widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control'}))