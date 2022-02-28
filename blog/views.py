from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Post, Comment
from .forms import PostForm, UserForm, CommentForm
from django.core.paginator import Paginator


def index(request):
    user_list = User.objects.all()
    return render(request, 'blog/index.html', {'users': user_list})


def post_list(request, id):
    page = request.GET.get('page', '1')  # 페이지

    posts = Post.objects.filter(user=id).order_by('-created_at')

    paginator = Paginator(posts, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'posts': page_obj, 'id': id}
    return render(request, 'blog/post_list.html', context)


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


@login_required(login_url='blog:login')
def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.user:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('blog:post_detail', id=request.user.id, post_id=post_id)
    else:
        post.delete()
    return redirect('blog:post_list', id=request.user.id)

@login_required(login_url='blog:login')
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


@login_required(login_url='blog:login')
def comment_create(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.created_at = timezone.now()
            comment.post = post
            comment.save()
            return redirect('blog:post_detail', id=request.user.id, post_id=post_id)
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'blog/comment_form.html', context)


@login_required(login_url='blog:login')
def comment_modify(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.user:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('blog:post_detail', id=request.user.id, post_id=comment.post.post_id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.modified_at = timezone.now()
            comment.save()
            return redirect('blog:post_detail', id=request.user.id, post_id=comment.post.post_id)
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'blog/comment_form.html', context)


@login_required(login_url='blog:login')
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.user:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('blog:post_detail', id=request.user.id, post_id=comment.post.post_id)
    else:
        print("ok")
        comment.delete()
    return redirect('blog:post_detail', id=request.user.id, post_id=comment.post.post_id)


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