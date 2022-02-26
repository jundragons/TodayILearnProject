from django.contrib import admin
from .models import Post
from .models import User
from .models import Categories
from .models import Comment

admin.site.register(Post)
admin.site.register(User)
admin.site.register(Categories)
admin.site.register(Comment)