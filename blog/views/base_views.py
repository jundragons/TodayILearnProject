from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from .post_views import post_list
from ..forms import UserForm


def index(request):
    if request.user.is_authenticated:
        return post_list(request, request.user.id)
    else:
        return render(request, 'blog/index.html')


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
            return redirect('blog:post_list', id=user.id)

    else:
        form = UserForm()
    return render(request, 'registration/signup.html', {'form': form})
