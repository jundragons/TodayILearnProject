from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect

from ..models import Categories


@login_required(login_url='blog:login')
def category_list(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.user != user:
        messages.error(request, '카테고리 삭제 권한이 없습니다')
        return redirect('blog:post_list', id=user_id)
    category = Categories.objects.filter(user_id=user_id)
    return render(request, 'blog/category_list.html', {'categories': category})


@login_required(login_url='blog:login')
def category_create(request, value):
    user = get_object_or_404(User, pk=request.user.id)
    if request.user != user:
        messages.error(request, '카테고리 삭제 권한이 없습니다')
        return redirect('blog:category_list', id=user.id)
    new_category = Categories(category=value, user=request.user)
    new_category.save()
    return redirect('blog:category_list', user_id=user.id)

@login_required(login_url='blog:login')
def category_modify(request, before, value):
    category = Categories.objects.get(category=before, user=request.user)
    category.category = value
    category.save()
    return redirect('blog:category_list', user_id=request.user.id)


@login_required(login_url='blog:login')
def category_delete(request, category_id):
    category = get_object_or_404(Categories, pk=category_id)
    if request.user != category.user:
        messages.error(request, '카테고리 삭제 권한이 없습니다')
        return redirect('blog:category_list', user_id=request.user.id)
    else:
        print("ok")
        category.delete()
    return redirect('blog:category_list', user_id=request.user.id)

