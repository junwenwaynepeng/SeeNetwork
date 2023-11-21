from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, UserProfileForm, SelfIntroductionForm, EducationForm, WorkExperienceForm, EssentialSkillForm, AwardForm, PublicationForm
from .models import CustomUser as User
from .models import WorkExperience, EssentialSkill, Award, Publication, CurriculumVitae, Education, SelfIntroduction
from operator import itemgetter
from dataclasses import dataclass
import json

@dataclass
class CVCard:
	title: str
	model: str
	is_list: bool
	item_list: list
	content: str

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
    
    # model: curricumlum vitae
    curriculum_vitae, created = CurriculumVitae.objects.get_or_create(user=profile_owner)
    
    # model: self introduction
    self_introduction, created = SelfIntroduction.objects.get_or_create(user=profile_owner)
    self_introduction_form = SelfIntroductionForm(instance=self_introduction)
    self_introduction_card = CVCard('自介', 'selfIntroduction', False, [], self_introduction.self_introduction)
    
    # model: education
    education_form = EducationForm()
    education = Education.objects.filter(user=profile_owner)
    education_card = CVCard('學歷', 'education', True, education, '')
    for edu in education:
	    print(edu)
    # model: work experience
    work_experience_form = WorkExperienceForm()
    work_experience = WorkExperience.objects.filter(user=profile_owner)
    work_experience_card = CVCard('工作經歷', 'workExperience', True, work_experience, '')

    # model: essential skill
    essential_skill_form = EssentialSkillForm()
    essential_skill = EssentialSkill.objects.filter(user=profile_owner)
    essential_skill_card = CVCard('專長', 'essentialSkill', True, essential_skill, '')
    
    # model: award
    award_form = AwardForm()
    award = Award.objects.filter(user=profile_owner)
    award_card = CVCard('獎項', 'award', True, award, '')
    
    # model: publication
    publication_form = PublicationForm()
    publication = Publication.objects.filter(user=profile_owner)
    publication_card = CVCard('文章', 'publication', True, publication, '')

    # setup cards
    card_order = [
    	(self_introduction_card, curriculum_vitae.self_introduction_form_order),
    	(education_card, curriculum_vitae.education_form_order),
    	(work_experience_card, curriculum_vitae.work_experience_form_order),
    	(essential_skill_card, curriculum_vitae.essential_skill_form_order),
    	(award_card, curriculum_vitae.award_form_order),
    	(publication_card, curriculum_vitae.publication_form_order),
    ]
    card_order = sorted(card_order, key=itemgetter(1))
    cards = [card[0] for card in card_order]

    return render(request, 'profile.html', {
        'profile_owner': profile_owner, 
        'profile_form': profile_form, 
        'cards': cards,
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
    self_introduction, created = SelfIntroduction.objects.get_or_create(user=user)
    if request.method == 'POST':
        self_introduction_form = SelfIntroductionForm(request.POST, instance=self_introduction)
        if self_introduction_form.is_valid():
            self_introduction_form.save()
    return profile_view(request, user.slug)

@login_required
def save_education(request):
    user = request.user
    if request.method == 'POST':
        education_form = EducationForm(request.POST)
        if education_form.is_valid():
            education = education_form.save(commit=False)
            education.user = user
            education.save()
    return profile_view(request, user.slug)

@login_required
def save_work_experience(request):
    user = request.user
    if request.method == 'POST':
        work_experience_form = WorkExperienceForm(request.POST)
        if work_experience_form.is_valid():
            work_experience = work_experience_form.save(commit=False)
            work_experience.user = user
            work_experience.save()
    return redirect('profile_view', user_slug=user.slug)

@login_required
def save_essential_skill(request):
    user = request.user
    if request.method == 'POST':
        essential_skill_form = EssentialSkillForm(request.POST)
        if essential_skill_form.is_valid():
            essential_skill = essential_skill_form.save(commit=False)
            essential_skill.user = user
            essential_skill.save()
    return redirect('profile_view', user_slug=user.slug)

@login_required
def save_award(request):
    user = request.user
    if request.method == 'POST':
        award_form = AwardForm(request.POST)
        if award_form.is_valid():
            award = award_form.save(commit=False)
            award.user = user
            award.save()
    return redirect('profile_view', user_slug=user.slug)

@login_required
def save_publication(request):
    user = request.user
    if request.method == 'POST':
        publication_form = PublicationForm(request.POST)
        if publication_form.is_valid():
            publication = publication_form.save(commit=False)
            publication.user = user
            publication.save()
    return redirect('profile_view', user_slug=user.slug)

@login_required
def delete_profile_item(request):
	user = request.user
	data = json.loads(request.body.decode('utf-8'))
	
	if data['model']=='education':
		item = Education.objects.get(id=data['itemId'])
		
	if data['model']=='workExperience':
		item = WorkExperience.objects.get(id=data['itemId'])
		
	if data['model']=='essentialSkill':
		item = EssentialSkill.objects.get(id=data['itemId'])

	if data['model']=='award':
		item = Award.objects.get(id=data['itemId'])

	if data['model']=='publication':
		item = Publication.objects.get(id=data['itemId'])

	item.delete()
	return redirect('profile_view', user_slug=user.slug)
