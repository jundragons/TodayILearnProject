from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Post, Categories
from .forms import PostForm, UserForm


def index(request):
    user_list = User.objects.all()
    return render(request, 'blog/index.html', {'users': user_list})


def post_list(request, id):
    posts = Post.objects.filter(user=id).order_by('-created_at')
    return render(request, 'blog/post_list.html',
                  {'posts': posts, 'id': id})

def post_detail(request, id, post_id):
    post = Post.objects.get(post_id=post_id)
    return render(request, 'blog/post_detail.html', {'post':post})

@login_required(login_url='blog:login')
def post_edit(request, id, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.user:
        messages.error(request, '수정권한이 없습니다')
        return redirect('blog:post_detail', id=id, post_id=post_id)

    if request.method == "POST":
        form = PostForm(request.user, request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.modified_at = timezone.now()  # 수정일시 저장
            post.save()
            return redirect('blog:post_detail', id=id, post_id=post_id)
    else:
        form = PostForm(request.user,instance=post)
    context = {'form': form}
    return render(request, 'blog/post_form.html', context)

def post_create(request, id):
    if request.method == "POST":
        form = PostForm(request.user, request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.created_at = timezone.now()
            post.modified_at = timezone.now()
            post.save()
            return redirect('blog:post_list', id=id)
    else:
        form = PostForm(request.user)

    return render(request, 'blog/post_form.html', {'form': form})


def signup(request):
    """
    계정생성
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('blog:index')
    else:
        form = UserForm()
    return render(request, 'registration/signup.html', {'form': form})