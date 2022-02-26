from django import forms
from .models import Categories, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'category', )
        labels = {
            'title': '제목',
            'content': '내용',
            'category': '카테고리'
        }
