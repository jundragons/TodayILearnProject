from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'blog'

urlpatterns = [
    # http://localhost:8080 (not login)
    path('', views.index, name='index'),
    # http://localhost:8080 (login)
    path('post/<int:id>/', views.post_list, name='post_list'),
    # http://localhost:8080/post/<int:user_id>/create/
    path('post/create/<int:id>', views.post_create, name='post_create'),
    # login
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html'), name='login'),
    #logout
    path('logout/', auth_views.LogoutView.as_view(),name='logout'),
    #signup
    path('signup/', views.signup, name='signup')
]