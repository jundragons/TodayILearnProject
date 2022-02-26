from django.db import models

# User Model
class User(models.Model):
    user_id = models.AutoField(primary_key = True)
    id = models.CharField(max_length=20)
    nickname = models.CharField(max_length=20)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'id: ' + self.id + \
               ' 닉네임:' + self.nickname

# Categories Model
class Categories(models.Model):
    category_id = models.AutoField(primary_key = True)
    category = models.CharField(max_length=20)
    user_id = models.ForeignKey('blog.User', on_delete=models.CASCADE,
                                related_name='categories')
    def __str__(self):
        return 'category_id: ' + self.category + \
               ' 소유자:' + self.user_id +\
               ' 카테고리: ' + self.category
# Post Model
class Post(models.Model):
    post_id = models.AutoField(primary_key = True)
    user_id = models.ForeignKey('blog.User', on_delete=models.CASCADE,
                                related_name='post')
    category_id = models.ForeignKey('blog.Categories', on_delete=models.CASCADE,
                                    related_name='post')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'post_id: ' + self.post_id + \
               ' user_id: ' + self.user_id + \
               ' title: ' + self.title + \
               ' category ' + self.category_id + \
               ' content ' + self.content

# Comment Model
class Comment(models.Model):
    comment_id = models.AutoField(primary_key = True)
    user_id = models.ForeignKey('blog.User', on_delete=models.CASCADE,
                                related_name='comment')
    post_id = models.ForeignKey('blog.Post', on_delete=models.CASCADE,
                                related_name='comment')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)