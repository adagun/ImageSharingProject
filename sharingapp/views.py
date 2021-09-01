from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from .models import Post
from .forms import PostForm
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

def indexView(request):
    return render(request, "index.html")


class PostsView(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = "posts"
    template_name = "posts/posts.html"


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('posts')
    template_name = "posts/post_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PostCreate, self).form_valid(form)


class PostEdit(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('posts')
    template_name = "posts/post_form.html"


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    context_object_name = 'post'
    success_url = reverse_lazy('posts')
    template_name = "posts/delete_post.html"


class PostView(LoginRequiredMixin, DetailView):
    model = Post
    context_object_name = "post"
    template_name = "posts/post.html"
