from django.contrib import admin
from .models import Trend
from .models import Post
from .models import PostAttachment
from .models import Like
from .models import Comment

# Register your models here.
admin.site.register(Trend)
admin.site.register(Post)
admin.site.register(PostAttachment)
admin.site.register(Like)
admin.site.register(Comment)
