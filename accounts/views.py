from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext as _
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from .forms import SignUpForm, UserProfileForm, SelfIntroductionForm, EducationForm, WorkExperienceForm, EssentialSkillForm, AwardForm, PublicationForm, SelfDefinedContentForm, PrivateSettingForm, ProfilePageSettingForm, ContactForm
from .models import CustomUser as User
from .models import WorkExperience, EssentialSkill, Award, Publication, CurriculumVitae, Education, SelfIntroduction, SelfDefinedContent, PrivateSetting, ProfilePageSetting, Contact
from operator import itemgetter
from dataclasses import dataclass
import json, re

@dataclass
class CVCard:
    card_id: int
    title: str
    edit_title: str
    order: int
    modal: str
    is_list: bool
    item_list: list(('typing.Any', 'typing.Any'))
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
    profile_page_setting, create = ProfilePageSetting.objects.get_or_create(user=profile_owner)
    if profile_page_setting.use_custom_page:
        return HttpResponseRedirect(profile_page_setting.url)

    profile_form = UserProfileForm(instance=profile_owner)
    
    # modal: curricumlum vitae
    curriculum_vitae, created = CurriculumVitae.objects.get_or_create(user=profile_owner)
    
    # modal: self introduction
    self_introduction, created = SelfIntroduction.objects.get_or_create(user=profile_owner)
    self_introduction_form = SelfIntroductionForm(instance=self_introduction)
    self_introduction_card = CVCard(None, '自介', '編輯自介', curriculum_vitae.self_introduction_form_order, 'selfIntroduction', False, list(zip([], [])), self_introduction.self_introduction, self_introduction_form)
    
    # modal: education
    education_form = EducationForm()
    education = Education.objects.filter(user=profile_owner)
    education_form_list = [EducationForm(instance=item) for item in education]
    education_card = CVCard(None, '學歷', '新增學歷', curriculum_vitae.education_form_order,'education', True, list(zip(education, education_form_list)), '', education_form)

    # modal: work experience
    work_experience_form = WorkExperienceForm()
    work_experience = WorkExperience.objects.filter(user=profile_owner)
    work_experience_form_list = [WorkExperienceForm(instance=item) for item in work_experience]
    work_experience_card = CVCard(None, '工作經歷', '新增工作經歷', curriculum_vitae.work_experience_form_order, 'workExperience', True, list(zip(work_experience, work_experience_form_list)), '', work_experience_form)

    # modal: essential skill
    essential_skill_form = EssentialSkillForm()
    essential_skill = EssentialSkill.objects.filter(user=profile_owner)
    essential_skill_form_list = [EssentialSkillForm(instance=item) for item in essential_skill]
    essential_skill_card = CVCard(None, '專長', '新增專長', curriculum_vitae.essential_skill_form_order, 'essentialSkill', True, list(zip(essential_skill, essential_skill_form_list)), '', essential_skill_form)
    
    # modal: award
    award_form = AwardForm()
    award = Award.objects.filter(user=profile_owner)
    award_form_list = [AwardForm(instance=item) for item in award]
    award_card = CVCard(None, '獎項', '新增獎項', curriculum_vitae.award_form_order, 'award', True, list(zip(award, award_form_list)), '', award_form)
    
    # modal: publication
    publication_form = PublicationForm()
    publication = Publication.objects.filter(user=profile_owner)
    publication_form_list = [PublicationForm(instance=item) for item in publication]
    publication_card = CVCard(None, '文章', '新增文章', curriculum_vitae.publication_form_order, 'publication', True, list(zip(publication, publication_form_list)), '', publication_form)

    # modal: self_defined_content
    self_defined_content_form = SelfDefinedContentForm()
    self_defined_content = SelfDefinedContent.objects.filter(user=profile_owner)
    self_defined_content_cards = []
    for card in self_defined_content:
        card_form = SelfDefinedContentForm(instance=card)
        self_defined_content_card = CVCard(card.id, card.title, f'修改{card.title}', card.form_order, f'selfDefinedContent{card.id}', False, list(zip([], [])), card.content, card_form)
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
def save_other_profile(request, modal):
    def extract_number_from_string(input_string):
        # Use regular expression to find the number at the end of the string
        match = re.search(r'\d+$', input_string)

        # Check if a match is found
        if match:
            return int(match.group())  # Convert the matched string to an integer
        else:
            return None  # Return None if no match is found
    
    user = request.user
    card_id = extract_number_from_string(modal)
    modal = re.sub(r'\d+$', '', modal)
    if request.method == 'POST':
        if modal == 'selfIntroduction':
            self_introduction, created = SelfIntroduction.objects.get_or_create(user=user)
            form = SelfIntroductionForm(request.POST, instance=self_introduction)
            
        if modal == 'education':
            form = EducationForm(request.POST)
        
        if modal == 'workExperience':
            form = WorkExperienceForm(request.POST)
        
        if modal == 'essentialSkill':
            form = EssentialSkillForm(request.POST)
            all_essential_skill = EssentialSkill.objects.filter(user=user)
            if all_essential_skill:
                order = max([obj.order for obj in all_essential_skill]) + 1
            else:
                order = 0
            
        if modal == 'award':
            form = AwardForm(request.POST)

        if modal == 'publication':
            form = PublicationForm(request.POST)

        if modal == 'selfDefinedContent':
            if card_id:
                self_defined_content = SelfDefinedContent.objects.get(id=card_id) 
                form = SelfDefinedContentForm(request.POST, instance=self_defined_content)
                order = self_defined_content.form_order
            else:
                form = SelfDefinedContentForm(request.POST)
                all_self_defined_content = SelfDefinedContent.objects.filter(user=user)
                if all_self_defined_content:
                    order = len(all_self_defined_content) + 6
                else:
                    order = 6
                
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = user
            if modal == 'essentialSkill':
                obj.order = order
            if modal == 'selfDefinedContent':
                obj.form_order = order
            obj.save()

    return HttpResponseRedirect(f"/profile/{user.slug}")

@login_required
def delete_profile_item(request):
    user = request.user
    data = json.loads(request.body.decode('utf-8'))
    modal = re.sub(r'\d+$', '', data['modal'])
    if modal == 'education':
        item = Education.objects.get(id=data['itemId'])
        
    if modal == 'workExperience':
        item = WorkExperience.objects.get(id=data['itemId'])
        
    if modal == 'essentialSkill':
        item = EssentialSkill.objects.get(id=data['itemId'])

    if modal == 'award':
        item = Award.objects.get(id=data['itemId'])

    if modal == 'publication':
        item = Publication.objects.get(id=data['itemId'])

    if modal == 'selfDefinedContent':
        item = SelfDefinedContent.objects.get(id=data['itemId'])

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
    new_order = [int(order) for order in new_order]
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

@login_required
def settings(request):
    user = request.user
    private_setting, created = PrivateSetting.objects.get_or_create(user=user)
    private_setting_form = PrivateSettingForm(instance=private_setting)
    profile_page_setting, created = ProfilePageSetting.objects.get_or_create(user=user)
    profile_page_setting_form = ProfilePageSettingForm(instance=profile_page_setting)
    contact, created = Contact.objects.get_or_create(user=user)
    contact_form = ContactForm(instance=contact)
    forms = {
        'private': {'title': _('Who can see me'), 'form': private_setting_form},
        'profilePage': {'title': _('Customize Profile Page'), 'form': profile_page_setting_form},
        'contact': {'title': _('Contact'), 'form': contact_form},
    }
    return render(request, 'settings.html', {'forms': forms})

@login_required
def save_setting(request, modal):
    user = request.user
    if request.method == 'POST':
        if modal == 'private':
            private_setting, created = PrivateSetting.objects.get_or_create(user=user)
            form = PrivateSettingForm(request.POST, instance=private_setting)
        if modal == 'profilePage':
            profile_page_setting, created = ProfilePageSetting.objects.get_or_create(user=user)
            form = ProfilePageSettingForm(request.POST, instance=profile_page_setting)
        if modal == 'contact':
            contact, created = Contact.objects.get_or_create(user=user)
            form = ContactForm(request.POST,instance=profile_page_setting)
        form.save()
    return HttpResponseRedirect("/settings")