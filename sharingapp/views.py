from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post, UserSavedImage
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


@login_required
def profileView(request):
    savedImages = UserSavedImage.objects.filter(user=request.user)
    postImages = Post.objects.filter(user=request.user)

    context = {
        "savedImages":savedImages,
        "postImages":postImages,
    }
    return render(request, "profile.html", context)

def userPage(request, Id):
    postImages = Post.objects.filter(user=Id)
    user = User.objects.get(id=Id)

    context = {
        "user":user,
        "postImages":postImages,
    }
    return render(request, "userPage.html", context)
