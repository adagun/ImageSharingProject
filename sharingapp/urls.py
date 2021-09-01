from django.urls import path
from . import views

urlpatterns = [

    path('posts/', views.PostsView.as_view(), name="posts"),
    path('', views.indexView, name="index"),
]
