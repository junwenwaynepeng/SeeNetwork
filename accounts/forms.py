from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import SelectDateWidget
from django.utils.translation import gettext as _
from crispy_forms.layout import Layout, Fieldset, Submit
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import Tab, TabHolder, FormActions
from .models import CustomUser as User
from .models import StudentSetting, CurriculumVitae, Education, WorkExperience, EssentialSkill, Award, Publication, SelfDefinedContent, SelfIntroduction, PrivateSetting, ProfilePageSetting
import datetime
from martor.widgets import MartorWidget


class PrivateSettingForm(forms.ModelForm):
    class Meta:
        model = PrivateSetting
        fields = ['display_name', 'display_student_id', 'display_nick_name', 'display_gender', 'display_department', 'display_cv']
        range_slider = forms.NumberInput(attrs={'type': 'range', 'min': '0', 'max': '6',  'class': "w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700"})
        widgets = {
            'display_name': range_slider,
            'display_student_id': range_slider,
            'display_nick_name': range_slider,
            'display_gender': range_slider,
            'display_department': range_slider,
            'display_cv': range_slider,
        }

class ProfilePageSettingForm(forms.ModelForm):
    class Meta:
        model = ProfilePageSetting
        fields = ['url', 'use_custom_page']

class StudentSettingForm(forms.ModelForm):
    class Meta:
        model = StudentSetting
        fields = ['student_id', 'department', 'degree', 'school']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'nick_name', 'gender', 'email']

class ContactForm(forms.ModelForm): 
    class Meta:
        model = User
        fields = ['facebook', 'x', 'instagram', 'linkedin', 'whatsapp', 'telegram', 'discord', 'tiktok', 'line', 'calendly', 'github', 'reddit', 'stackoverflow', 'youtube', 'spotify', 'telephone', 'steam', 'twitch', 'orcid', 'google_scholar', 'patreon', 'medium', 'line']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'contact-modal'
        self.helper.method = 'post'
        self.helper.form_action = "/save_profile/contact"
        self.helper.layout = Layout(
            TabHolder(
                Tab(_('Common'),
                    'instagram',
                    'facebook',
                    'x',
                    'tiktok',
                    'line',
                    'telephone',
                    'whatsapp'
                ),
                Tab(_('For work'),
                    'linkedin',
                    'calendly',
                    'github'
                ),
                Tab(_('For academe'),
                    'orcid',
                    'google_scholar'
                ),
                Tab(_('For entertainment'),
                    'discord',
                    'tiktok',
                    'youtube',
                    'spotify',
                    'steam',
                    'twitch',
                ),
                Tab(_('Others'),
                    'reddit',
                    'stackoverflow',
                    'patreon',
                    'medium',
                    'telegram'
                ),
            )
        )
        self.helper.add_input(
            Submit('submit', 'Save', css_class='rounded-md bg-indigo-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600'
            )
        )


class SelfIntroductionForm(forms.ModelForm):
    class Meta:
        model = SelfIntroduction
        fields = ['self_introduction']

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['school', 'department', 'degree', 'year']
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



