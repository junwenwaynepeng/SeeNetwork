from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import SelectDateWidget
from crispy_forms.layout import Layout, Fieldset, Submit
from crispy_forms.helper import FormHelper
from .models import CustomUser as User
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

    def __init__(self, *args, **kwargs):
        super(WorkExperienceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))

        # Customize the widget for the start_date field
        self.fields['start_date'].widget = SelectDateWidget(years=range(1990, 2030))

class EssentialSkillForm(forms.ModelForm):
    class Meta:
        model = EssentialSkill
        fields = ['skill_name', 'description']

class AwardForm(forms.ModelForm):
    class Meta:
        model = Award
        fields = ['title', 'organization', 'year', 'high_light']

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

