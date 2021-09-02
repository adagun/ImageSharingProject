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
    path('post/<int:pk>/', views.PostView.as_view(), name="post"),
    path('searchbar/', views.searchbar, name="searchbar"),
    path('save_post/<int:Id>/', views.savePost, name="save_post"),
    path('follow_user/<int:Id>/', views.followUser, name="follow_user"),
    path('delete_follow_user/<int:Id>/', views.deleteFollowUser, name="delete_follow_user"),
    path('followed_user_page/', views.followedUserPage, name="followed_user_page"),
    path('unsave_post/<int:Id>/', views.unsavePost, name="unsave_post"),
    path('edit_profile_picture/<int:pk>/', views.EditProfilePicture.as_view(), name="edit_profile_picture"),

]
