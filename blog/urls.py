from django.urls import path
from django.contrib.auth import views as auth_views
from .views import base_views, post_views, comment_views, category_views

app_name = 'blog'

urlpatterns = [
    # http://localhost:8080 (not login)
    path('', base_views.index, name='index'),
    # post_list (user)
    path('post/<int:id>/', post_views.post_list, name='post_list'),
    # post create
    path('post/create/<int:id>', post_views.post_create, name='post_create'),
    # post detail
    path('post/<int:id>/<int:post_id>', post_views.post_detail, name='post_detail'),
    # post edit
    path('post/edit/<int:id>/<int:post_id>', post_views.post_edit, name='post_edit'),
    # post delete
    path('post/delete/<int:post_id>', post_views.post_delete, name='post_delete'),
    # comment create
    path('comment/create/<int:post_id>/', comment_views.comment_create, name='comment_create'),
    # comment edit
    path('comment/modify/<int:comment_id>/', comment_views.comment_modify, name='comment_modify'),
    # comment delete
    path('comment/delete/<int:comment_id>/', comment_views.comment_delete, name='comment_delete'),
    # category list
    path('category/<int:user_id>/', category_views.category_list, name='category_list'),
    # category create
    path('category/create/<str:value>/', category_views.category_create, name='category_create'),
    # category modify
    path('category/modify/<str:before>/<str:value>/', category_views.category_modify, name='category_modify'),
    # category delete
    path('category/delete/<int:category_id>/', category_views.category_delete, name='category_delete'),
    # login
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html'), name='login'),
    # logout
    path('logout/', auth_views.LogoutView.as_view(),name='logout'),
    # signup
    path('signup/', base_views.signup, name='signup')
]