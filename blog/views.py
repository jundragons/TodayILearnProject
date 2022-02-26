# from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import User, Post
from .forms import PostForm

def index(request):
    user_list = User.objects.all()
    return render(request, 'blog/index.html', {'users' : user_list})


def post_list(request, user_id):
    posts = Post.objects.filter(user_id = user_id).order_by('-created_at')
    return render(request, 'blog/post_list.html',
                  {'posts' : posts})


def post_create(request):
    form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})