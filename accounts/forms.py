from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser as User
from crispy_forms.layout import Layout, Fieldset, Submit
from crispy_forms.helper import FormHelper
from .models import WorkExperience, SelfIntroduction, EssentialSkill, Award, Publication, SelfDefinedContent

class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperience
        fields = ['position', 'company', 'start_date', 'end_date', 'description']

class SelfIntroductionForm(forms.ModelForm):
    class Meta:
        model = SelfIntroduction
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }


class EssentialSkillForm(forms.ModelForm):
    class Meta:
        model = EssentialSkill
        fields = ['skill_name']

class AwardForm(forms.ModelForm):
    class Meta:
        model = Award
        fields = ['title', 'year']

class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ['title', 'authors', 'publication_date']

class SelfDefinedContent(forms.ModelForm):
    class Meta:
        model = SelfDefinedContent
        fields = ['title', 'content']

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

