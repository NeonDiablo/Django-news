from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('news/<int:pk>/', views.single_news, name='single_news'),
    path('news/category/<slug:slug>/', views.category_news, name='category_news'),
    path('news/search/', views.search_news, name='search_news'),
    path('login/', views.news_login, name='news_login'),
    path('logout/', views.news_logout, name='news_logout'),
    path('register/', views.news_register, name='news_register'),
    path('news/create/', views.create_news, name='create_news'),
    path('news/<int:pk>/change/', views.change_news, name='change_news'),
    path('news/<int:pk>/delete/', views.delete_news, name='delete_news'),
    path('account/<int:userpk>/', views.user_account, name='user_account'),
    path('account/<int:userpk>/news/', views.user_news, name='user_news'),
]
