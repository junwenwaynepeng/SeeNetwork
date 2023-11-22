from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from .forms import SignUpForm, UserProfileForm, SelfIntroductionForm, EducationForm, WorkExperienceForm, EssentialSkillForm, AwardForm, PublicationForm, SelfDefinedContentForm
from .models import CustomUser as User
from .models import WorkExperience, EssentialSkill, Award, Publication, CurriculumVitae, Education, SelfIntroduction, SelfDefinedContent
from operator import itemgetter
from dataclasses import dataclass
import json, re

@dataclass
class CVCard:
    title: str
    edit_title: str
    order: int
    model: str
    is_list: bool
    item_list: list
    content: str
    form: 'typing.Any'

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
    self_introduction_card = CVCard('自介', '編輯自介', curriculum_vitae.self_introduction_form_order, 'selfIntroduction', False, [], self_introduction.self_introduction, self_introduction_form)
    
    # model: education
    education_form = EducationForm()
    education = Education.objects.filter(user=profile_owner)
    education_card = CVCard('學歷', '新增學歷', curriculum_vitae.education_form_order,'education', True, education, '', education_form)

    # model: work experience
    work_experience_form = WorkExperienceForm()
    work_experience = WorkExperience.objects.filter(user=profile_owner)
    work_experience_card = CVCard('工作經歷', '新增工作經歷', curriculum_vitae.work_experience_form_order, 'workExperience', True, work_experience, '', work_experience_form)

    # model: essential skill
    essential_skill_form = EssentialSkillForm()
    essential_skill = EssentialSkill.objects.filter(user=profile_owner)
    essential_skill_card = CVCard('專長', '新增專長', curriculum_vitae.essential_skill_form_order, 'essentialSkill', True, essential_skill, '', essential_skill_form)
    
    # model: award
    award_form = AwardForm()
    award = Award.objects.filter(user=profile_owner)
    award_card = CVCard('獎項', '新增獎項', curriculum_vitae.award_form_order, 'award', True, award, '', award_form)
    
    # model: publication
    publication_form = PublicationForm()
    publication = Publication.objects.filter(user=profile_owner)
    publication_card = CVCard('文章', '新增文章', curriculum_vitae.publication_form_order, 'publication', True, publication, '', publication_form)

    # model: self_defined_content
    self_defined_content_form = SelfDefinedContentForm()
    self_defined_content = SelfDefinedContent.objects.filter(user=profile_owner)
    self_defined_content_cards = []
    for card in self_defined_content:
        card_form = SelfDefinedContentForm(instance=card)
        self_defined_content_card = CVCard(card.title, f'修改{card.title}', card.form_order, f'selfDefinedContent{card.id}', False, [], card.content, card_form)
        self_defined_content_cards.append((self_defined_content_card, self_defined_content_card.order))
    # setup cards
    card_order = [
        (self_introduction_card, curriculum_vitae.self_introduction_form_order),
        (education_card, curriculum_vitae.education_form_order),
        (work_experience_card, curriculum_vitae.work_experience_form_order),
        (essential_skill_card, curriculum_vitae.essential_skill_form_order),
        (award_card, curriculum_vitae.award_form_order),
        (publication_card, curriculum_vitae.publication_form_order),
    ] + self_defined_content_cards
    card_order = sorted(card_order, key=itemgetter(1))
    cards = [card[0] for card in card_order]

    return render(request, 'profile.html', {
        'profile_owner': profile_owner, 
        'profile_form': profile_form, 
        'cards': cards,
        'empty_self_defined_content_form': self_defined_content_form,
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
    return HttpResponseRedirect(f"/profile/{user.slug}")

@login_required
def save_other_profile(request, model):
    user = request.user
    model = re.sub(r'\d+$', '', model)
    if request.method == 'POST' or request.method == 'UPDATE':
        if model == 'selfIntroduction':
            self_introduction, created = SelfIntroduction.objects.get_or_create(user=user)
            self_introduction_form = SelfIntroductionForm(request.POST, instance=self_introduction)
            if self_introduction_form.is_valid():
                self_introduction_form.save()

        if model == 'education':
            form = EducationForm(request.POST)
        
        if model == 'workExperience':
            form = WorkExperienceForm(request.POST)
        
        if model == 'essentialSkill':
            form = EssentialSkillForm(request.POST)
            all_essential_skill = EssentialSkill.objects.filter(user=user)
            if all_essential_skill:
                order = max([obj.order for obj in all_essential_skill]) + 1
            else:
                order = 0
            
        if model == 'award':
            form = AwardForm(request.POST)

        if model == 'publication':
            form = PublicationForm(request.POST)

        if model == 'selfDefinedContent':
            form = SelfDefinedContentForm(request.POST)
            if request.method == 'POST':
                all_self_defined_content = SelfDefinedContent.objects.filter(user=user)
                if all_self_defined_content:
                    order = len(all_self_defined_content) + 6
                else:
                    order = 6

        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = user
            if model == 'essentialSkill':
                obj.order = order
            if model == 'selfDefinedContent' and request.method == 'POST':
                obj.form_order = order
            obj.save()

    return HttpResponseRedirect(f"/profile/{user.slug}")

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

@login_required
def save_cv_card_order(request):
    def is_self_defined(card_name):
        if re.sub(card_name, r'_\d+$', '') == 'self_defined_content':
            return True
        else:
            return False
    user = request.user
    new_order = json.loads(request.body.decode('utf-8'))['cvCard']
    new_order = [eval(order) for order in new_order]
    curriculum_vitae, created = CurriculumVitae.objects.get_or_create(user=user)
    self_defined_content = SelfDefinedContent.objects.filter(user=user)
    self_defined_content_cards = [[card, card.form_order] for card in self_defined_content]
    predefined_cards =[[field.name, getattr(curriculum_vitae, field.name)] for field in CurriculumVitae._meta.get_fields() if type(getattr(curriculum_vitae, field.name))==int and field.name!='id']
    cards = sorted(self_defined_content_cards + predefined_cards, key=itemgetter(1))
    for card in cards:
        if type(card[0]) is str:
            setattr(curriculum_vitae, card[0], new_order.index(card[1]))
        else:
            card[0].form_order = new_order.index(card[1])
            card[0].save()
    curriculum_vitae.save()
    return JsonResponse({'message': 'mark all notification as read'})