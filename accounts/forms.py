from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import SelectDateWidget
from crispy_forms.layout import Layout, Fieldset, Submit
from crispy_forms.helper import FormHelper
from .models import CustomUser as User
from .models import CurriculumVitae, Education, WorkExperience, EssentialSkill, Award, Publication, SelfDefinedContent, SelfIntroduction, PrivateSetting, ProfilePageSetting, Contact
import datetime

class PrivateSettingForm(forms.ModelForm):
    class Meta:
        model = PrivateSetting
        fields = ['display_name', 'display_student_id', 'display_nick_name', 'display_gender', 'display_department', 'display_cv']
        widget ={
            'display_name': forms.NumberInput(attrs={'type': 'range', 'class': 'form-range', 'step': '1', 'min': '0', 'max': '6', 'id':'displayName'}),
            'display_student_id': forms.NumberInput(attrs={'type': 'range', 'class': 'form-range', 'step': '1', 'min': '0', 'max': '6', 'id':'displayStudentId'}),
            'display_nick_name': forms.NumberInput(attrs={'type': 'range', 'class': 'form-range', 'step': '1', 'min': '0', 'max': '6', 'id':'displayNickName'}),
            'display_gender': forms.NumberInput(attrs={'type': 'range', 'class': 'form-range', 'step': '1', 'min': '0', 'max': '6', 'id':'displayGender'}),
            'display_department': forms.NumberInput(attrs={'type': 'range', 'class': 'form-range', 'step': '1', 'min': '0', 'max': '6', 'id':'displayDepartment'}),
            'display_cv': forms.NumberInput(attrs={'type': 'range', 'class': 'form-range', 'step': '1', 'min': '0', 'max': '6', 'id':'displayCV'}),
        }

class ProfilePageSettingForm(forms.ModelForm):
    class Meta:
        model = ProfilePageSetting
        fields = ['url', 'use_custom_page']

class ContactForm(forms.ModelForm): 
    class Meta:
        model = Contact
        fields = ['facebook', 'twitter', 'instagram', 'linkedin', 'snapchat', 'whatsapp', 'telegram', 'skype', 'discord', 'tiktok', 'line']

class SelfIntroductionForm(forms.ModelForm):
    class Meta:
        model = SelfIntroduction
        fields = ['self_introduction']

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['school', 'degree', 'year']
        widgets = {
            'year': forms.NumberInput(attrs={'value': datetime.datetime.now().year}),
        }

class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperience
        fields = ['position', 'company', 'start_date', 'end_date', 'detail']
        widgets = {
            'position': forms.widgets.TextInput(attrs={'class': 'rounded'}),
            'start_date':  forms.widgets.DateInput(attrs={'type': 'date', 'class': 'rounded'}),
            'end_date':  forms.widgets.DateInput(attrs={'type': 'date',  'class': 'rounded'}),
        }

    def __init__(self, *args, **kwargs):
        super(WorkExperienceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))

        # Customize the widget for the start_date field


class EssentialSkillForm(forms.ModelForm):
    class Meta:
        model = EssentialSkill
        fields = ['skill_name', 'description']

class AwardForm(forms.ModelForm):
    class Meta:
        model = Award
        fields = ['title', 'organization', 'year', 'high_light']
        widgets = {
            'year': forms.NumberInput(attrs={'value': datetime.datetime.now().year}),
        }

class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ['title', 'authors', 'publication_date', 'link', 'high_light']

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

