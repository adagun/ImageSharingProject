from django.urls import path
from . import views

urlpatterns = [

    path('posts/', views.PostsView.as_view(), name="posts"),
    path('', views.indexView, name="index"),
    path('edit_post/<int:pk>/', views.PostEdit.as_view(), name="edit_post"),
    path('delete_post/<int:pk>/', views.PostDelete.as_view(), name="delete_post"),
    path('create_post/', views.PostCreate.as_view(), name="create_post"),
    path('post/<int:pk>/', views.PostView.as_view(), name="post")
]
