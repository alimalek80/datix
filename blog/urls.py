from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/new', views.post_create, name='post_create'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),

    path('post/<slug:slug>/edit/', views.post_edit, name='post_edit'),
    path('category/<slug:slug>/', views.posts_by_category, name='posts_by_category'),
    path('tag/<slug:slug>/', views.posts_by_tag, name='posts_by_tag'),
]