from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.utils import timezone

from ..forms import PostForm
from ..models import Post, Categories


def post_list(request, id):
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    ca = request.GET.get('ca', '')  # 카테고리 정렬
    so = request.GET.get('so', 'recent')  # 정렬기준

    # 정렬
    if so == 'recent':
        posts = Post.objects.filter(user=id).order_by('-created_at')
    else:   #오래된순
        posts = Post.objects.filter(user=id).order_by('created_at')

    # 카테고리별 검색
    if ca:
        posts = posts.filter(category=ca)

    elif kw:
        posts = posts.filter(
            Q(title__icontains=kw) |  # 제목검색
            Q(content__icontains=kw)  # 내용검색
        ).distinct()

    paginator = Paginator(posts, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    category = Categories.objects.filter(user=id)
    context = {'posts': page_obj, 'id': id, 'category': category, 'page': page, 'kw': kw, 'so': so}
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
        form = PostForm(request.user, instance=post)
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

