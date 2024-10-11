from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Follow
from .forms import  ProfileEditForm

def user_registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)

            return redirect('post_list')
    else:
        form = UserCreationForm()

    return render(request, 'registration.html', {'form': form})


def user_profile_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, user=user)

    is_following = Follow.objects.filter(follower=request.user, following=user).exists()

    followers = user.followers.all()
    following = user.following.all()

    return render(request, 'profile.html', {
        'profile': profile,
        'user': user,
        'is_following': is_following,
        'followers': followers,
        'following': following,
    })


@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)

    if user_to_follow == request.user:
        return HttpResponseForbidden("You cannot follow yourself.")

    if not Follow.objects.filter(follower=request.user, following=user_to_follow).exists():
        Follow.objects.create(follower=request.user, following=user_to_follow)

    return redirect('profile', user_id=user_id)


@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)

    if user_to_unfollow == request.user:
        return HttpResponseForbidden("You cannot unfollow yourself.")

    follow = Follow.objects.filter(follower=request.user, following=user_to_unfollow)
    follow.delete()

    return redirect('profile', user_id=user_id)


@login_required
def edit_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.user != user:
        return HttpResponseForbidden("You cannot edit another user's profile.")

    profile = user.profile

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', user_id=user.id)
    else:
        form = ProfileEditForm(instance=profile)

    return render(request, 'profile.html', {'form': form, 'profile': profile})
