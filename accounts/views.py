from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from .forms import SignUpForm, UserProfileForm
from .models import CustomUser as User

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
    user = request.user
    profile_owner = get_object_or_404(User, slug=user_slug)
    profile_form = UserProfileForm(instance=profile_owner)
    if request.method == 'GET':
    	show_current_profile=True
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=user)
        if profile_form.is_valid():
            profile_form.save()
    
    return render(request, 'profile.html', {'profile_owner': profile_owner, 'profile_form': profile_form, 'slug': user_slug})
