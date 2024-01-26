from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Profile, CustomUser
from .forms import (
    CustomUserCreationForm,
    CustomUserChangeForm,
    ProfileForm,
    PatientCreationForm,
)
from django.contrib import messages


@login_required
def user_update(request):
    if request.method == "POST":
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Your profile was successfully updated!")
            return redirect("home")

    else:
        user_form = CustomUserChangeForm(instance=request.user)

    context = {"user_form": user_form}
    return render(request, "accounts/user_update.html", context)


@login_required
def user_profile(request):
    if request.method == "POST":
        profile_form = ProfileForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, "Your profile was successfully updated!")
            return redirect("home")
    else:
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            profile = None

        if profile:
            profile_form = ProfileForm(instance=request.user.profile)
        else:
            profile_form = ProfileForm()

    return render(request, "accounts/user_profile.html", {"profile_form": profile_form})


def new_patient(request):
    if request.method == "POST":
        user_form = PatientCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            login(request, user)
            return redirect("home")
    else:
        user_form = PatientCreationForm()

    return render(request, "accounts/new_patient.html", {"user_form": user_form})
