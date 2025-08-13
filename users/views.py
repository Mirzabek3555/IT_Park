from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, CustomUserChangeForm, ProfileForm
from .models import Profile

def register(request):
    """Ro'yxatdan o'tish"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Profil yaratish
            Profile.objects.create(user=user)
            # Avtomatik login
            login(request, user)
            messages.success(request, 'Muvaffaqiyatli ro\'yxatdan o\'tdingiz!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile_edit(request):
    """Profilni tahrirlash"""
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            messages.success(request, 'Profil muvaffaqiyatli yangilandi!')
            return redirect('main:profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    
    return render(request, 'users/profile_edit.html', {'form': form, 'profile_form': profile_form})
