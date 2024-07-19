from django.contrib import admin
from .models import User
from .models import FriendshipRequest

# Register your models here.

admin.site.register(User)
admin.site.register(FriendshipRequest)