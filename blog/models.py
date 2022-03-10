from django.db import models
from django.contrib.auth.models import User


# Categories Model
class Categories(models.Model):
    category_id = models.AutoField(primary_key = True)
    category = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return self.category


# Post Model
class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('blog.Categories', on_delete=models.SET_NULL, null=True,
                                 related_name='post')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + ' : ' + self.title


# Comment Model
class Comment(models.Model):
    comment_id = models.AutoField(primary_key = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE,
                             related_name='comment')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content + ' 글번호 :' + str(self.post.post_id)
