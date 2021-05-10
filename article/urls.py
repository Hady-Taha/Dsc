from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('category/<slug:slug>', views.category, name='category'),
    path('article/<slug:slug>', views.article, name='article'),
    path('like/', views.like, name='like'),
    path('search/', views.search, name='search'),
    path('saveArticle/', views.saveArticle, name='saveArticle'),
    
]
