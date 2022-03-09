from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Categories, Comment


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'content', 'category')

    def __init__(self, user, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Categories.objects.filter(user=user)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '댓글내용',
        }


class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')