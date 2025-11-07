from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Profile # Import Profile model
from django.core.exceptions import ObjectDoesNotExist # Import ObjectDoesNotExist for clean error handling

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Welcome {username}, your account has been created succesfully!')
            return redirect('login')

    form = RegisterForm()        
    return render(request, 'users/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return render(request, 'users/logout.html')

@login_required
def profile(request):
    return render(request, 'users/profile.html')

@login_required
def profile_update(request):
    # DEFENSIVE FIX: Check and create a profile if it doesn't exist for the user
    try:
        user_profile = request.user.profile
    except ObjectDoesNotExist:
        # Create a profile with default values if it doesn't exist
        user_profile = Profile.objects.create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        # Use the ensured user_profile instance
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=user_profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        # Use the ensured user_profile instance
        p_form = ProfileUpdateForm(instance=user_profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'title': 'Update Profile'
    }

    return render(request, 'users/profile_update.html', context)