from django.shortcuts import render
from django.views.generic import ListView

from .models import Post
from .forms import PostForm
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class PostsView(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = "posts"
    template_name = "posts/posts.html"



