from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser as User
from crispy_forms.layout import Layout, Fieldset, Submit
from crispy_forms.helper import FormHelper

class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UserProfileForm(forms.ModelForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    class Meta:
        model = User
        fields = ['student_id', 'first_name', 'last_name', 'nick_name', 'gender', 'department', 'email']



