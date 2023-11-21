from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, UserProfileForm, SelfIntroductionForm, EducationForm
from .models import CustomUser as User
from .models import WorkExperience, EssentialSkill, Award, Publication, CurriculumVitae, Education


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def profile_view(request, user_slug):
    profile_owner = get_object_or_404(User, slug=user_slug)
    profile_form = UserProfileForm(instance=profile_owner)
    curriculum_vitae, created = CurriculumVitae.objects.get_or_create(user=profile_owner)
    self_introduction_form = SelfIntroductionForm(instance=curriculum_vitae)
    education_form = EducationForm()
    education = curriculum_vitae.education.all()
    #essential_skill = EssentialSkill.objects.filter(user=profile_owner).first()
    return render(request, 'profile.html', {
        'profile_owner': profile_owner, 
        'profile_form': profile_form, 
        'self_introduction_form': self_introduction_form,
        'curriculum_vitae': curriculum_vitae,
        'education_form': education_form,
        'education': education,
        #'essential_skill_form': essential_skill_form,
        'slug': user_slug
        })

@login_required
def save_profile(request):
    user = request.user
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=user)
        if profile_form.is_valid():
            profile_form.save()
    return profile_view(request, user.slug)

@login_required
def save_self_introduction(request):
    user = request.user
    curriculum_vitae, created = CurriculumVitae.objects.get_or_create(user=user)
    if request.method == 'POST':
        curriculum_vitae_form = SelfIntroductionForm(request.POST, instance=curriculum_vitae)
        if curriculum_vitae_form.is_valid():
            curriculum_vitae_form.save()
    return profile_view(request, user.slug)

@login_required
def save_education(request):
    user = request.user
    curriculum_vitae, created = CurriculumVitae.objects.get_or_create(user=user)
    print(created)
    if request.method == 'POST':
        education_form = EducationForm(request.POST)
        if education_form.is_valid():
            education_data = education_form.cleaned_data
            education = Education.objects.create(
                school=education_data['school'],
                degree=education_data['degree'],
                year=education_data['year']
            )
            education.save()
            curriculum_vitae.education.add(education)

            
    return profile_view(request, user.slug)