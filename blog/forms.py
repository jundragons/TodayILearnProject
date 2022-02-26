from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import  Post, User


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'category', )
        labels = {
            'title': '제목',
            'content': '내용',
            'category': '카테고리'
        }

class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email")