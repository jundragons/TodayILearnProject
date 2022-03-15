from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.utils import timezone

from ..forms import CommentForm
from ..models import Post, Comment


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

