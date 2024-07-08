from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import BusinessMessage

@login_required
def feed(request):
    userids = [request.user.id]

    for oinker in request.user.oinkerprofile.follows.all():
        userids.append(oinker.user.id)

    posts = BusinessMessage.objects.filter(created_by_id__in=userids)

    for post in posts:
        likes = post.likes.filter(created_by_id=request.user.id)

        if likes.count() > 0:
            post.liked = True
        else:
            post.liked = False

    return render(request, 'feed/feed.html', {'oinks': posts})

@login_required
def search(request):
    query = request.GET.get('query', '')

    if len(query) > 0:
        users = User.objects.filter(username__icontains=query)
        user_account = BusinessMessage.objects.filter(body__icontains=query)
    else:
        users = []
        user_account = []

    context = {
        'query': query,
        'oinkers': users,
        'oinks': user_account
        }

    return render(request, 'feed/search.html', context)
