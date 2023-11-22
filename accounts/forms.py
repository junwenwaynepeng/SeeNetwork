from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser as User
from crispy_forms.layout import Layout, Fieldset, Submit
from crispy_forms.helper import FormHelper
from .models import CurriculumVitae, Education, WorkExperience, EssentialSkill, Award, Publication, SelfDefinedContent, SelfIntroduction

class SelfIntroductionForm(forms.ModelForm):
    class Meta:
        model = SelfIntroduction
        fields = ['self_introduction']

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['school', 'degree', 'year']

class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperience
        fields = ['position', 'company', 'start_date', 'end_date', 'description']

class EssentialSkillForm(forms.ModelForm):
    class Meta:
        model = EssentialSkill
        fields = ['skill_name', 'description']

class AwardForm(forms.ModelForm):
    class Meta:
        model = Award
        fields = ['title', 'organization', 'year']

class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ['title', 'authors', 'publication_date']

class SelfDefinedContentForm(forms.ModelForm):
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

