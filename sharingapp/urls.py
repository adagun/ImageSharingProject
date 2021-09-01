from django.urls import path
from . import views

urlpatterns = [

    path('posts/', views.PostsView.as_view(), name="posts"),
    path('', views.indexView, name="index"),
    path('profile/', views.profileView, name="profile"),
    path('edit_post/<int:pk>/', views.PostEdit.as_view(), name="edit_post"),
    path('delete_post/<int:pk>/', views.PostDelete.as_view(), name="delete_post"),
    path('create_post/', views.PostCreate.as_view(), name="create_post"),
    path('userPage/<int:Id>/', views.userPage, name="userPage"),
]
