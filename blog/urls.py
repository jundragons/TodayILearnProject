from django.urls import path
from . import views

urlpatterns = [
    # http://localhost:8080 (not login)
    path('', views.index, name='index'),
    # http://localhost:8080 (login)
    path('post/<int:user_id>/', views.post_list, name='post_list'),
    # http://localhost:8080/post/<int:user_id>/create/
    path('post/<int:user_id>/create/', views.post_create, name='post_create')
]