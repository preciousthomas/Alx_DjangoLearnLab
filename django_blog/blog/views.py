# blog/views.py (append or add)

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, ProfileForm

def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # log the user in after registration
            login(request, user)
            return redirect("blog:profile")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {"form": form})

@login_required
def profile_view(request):
    profile = request.user.profile
    if request.method == "POST":
        pform = ProfileForm(request.POST, request.FILES, instance=profile)
        if pform.is_valid():
            pform.save()
            return redirect("blog:profile")
    else:
        pform = ProfileForm(instance=profile)

    return render(request, "blog/profile.html", {"pform": pform})