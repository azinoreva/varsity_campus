from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from apps.notification.utilities import create_notification

from .forms import UserProfileForm

def userprofile(request, username):
    user = get_object_or_404(User, username=username)
    oinks = user.oinks.all()

    for oink in oinks:
        likes = oink.likes.filter(created_by_id=request.user.id)

        if likes.count() > 0:
            oink.liked = True
        else:
            oink.liked = False

    context = {
        'user': user,
        'oinks': oinks
        }

    return render(request, 'userprofile/userprofile.html', context)

@login_required
def edit_profile(request):
        if request.method == 'POST':
            form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)

            if form.is_valid():
                form.save()

                return redirect('userprofile', username=request.user.username)
            else:
                form = UserProfileForm(instance=request.user.userprofile)
                                                        
            context = {
                'user': request.user,
                'form': form
            }

            return render(request, 'userprofile/edit_profile.html', context)

@login_required
def follow_user(request, username):
    user = get_object_or_404(User, username=username)

    request.user.userprofile.follows.add(user.userprofile)

    create_notification(request, user, 'follower')

    return redirect('userprofile', username=username)

@login_required
def unfollow_user(request, username):
    user = get_object_or_404(User, username=username)

    request.user.userprofile.follows.remove(user.userprofile)

    return redirect('userprofile', username=username)

def followers(request, username):
    user = get_object_or_404(User, username=username)

    return render(request, 'userprofile/followers.html', {'user': user})

def follows(request, username):
    user = get_object_or_404(User, username=username)

    return render(request, 'userprofile/follows.html', {'user': user})
