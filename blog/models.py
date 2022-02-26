from django.db import models


# User Model
class User(models.Model):
    user_id = models.AutoField(primary_key = True)
    id = models.CharField(max_length=20)
    nickname = models.CharField(max_length=20)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nickname +'(' + str(self.id) + ')'


# Categories Model
class Categories(models.Model):
    category_id = models.AutoField(primary_key = True)
    category = models.CharField(max_length=20)
    user = models.ForeignKey('blog.User', on_delete=models.CASCADE,
                                related_name='categories')

    def __str__(self):
        return self.category


# Post Model
class Post(models.Model):
    post_id = models.AutoField(primary_key = True)
    user = models.ForeignKey('blog.User', on_delete=models.CASCADE,
                                related_name='post')
    category = models.ForeignKey('blog.Categories', on_delete=models.CASCADE,
                                    related_name='post')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.nickname + ' : ' + self.title


# Comment Model
class Comment(models.Model):
    comment_id = models.AutoField(primary_key = True)
    user = models.ForeignKey('blog.User', on_delete=models.CASCADE,
                                related_name='comment')
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE,
                                related_name='comment')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content + ' 글번호 :' + str(self.post.post_id)
