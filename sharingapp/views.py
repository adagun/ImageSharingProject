
from django.http import request
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post, UserSavedImage
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.db.models import Q
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
    savedImages = UserSavedImage.objects.filter(user=request.user).order_by('-post__uploaded')
    postImages = Post.objects.filter(user=request.user).order_by('-uploaded')

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
class PostView(LoginRequiredMixin, DetailView):
    model = Post
    context_object_name = "post"
    template_name = "posts/post.html"

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)

        # get ids of posts in the users UserSavedImage set
        user_saved_set = self.request.user.usersavedimage_set.all().values_list('post', flat=True)
        if context["object"].id in user_saved_set:
            context['user_has_saved'] = True

        return context

def searchbar(request):
    if request.method == 'GET':
        query= request.GET.get('q')
        submitbutton= request.GET.get('submit')
        
        if query is not None:
            lookups= Q(title__icontains=query) | Q(description__icontains=query) | Q(user__username__icontains=query)
            results= Post.objects.filter(lookups).distinct()
            context={'results': results, 'submitbutton': submitbutton}
            return render(request, "posts/search_post.html", context)
        else:
            return render(request, "posts/search_post.html")
    else:
        return render(request, "posts/search_post.html")


def savePost(request, Id):
    post = Post.objects.get(id=Id)
    savedImages = UserSavedImage()
    exists = UserSavedImage.objects.filter(post=post, user=request.user)
    if not exists:
        savedImages.user=request.user
        savedImages.post=post
        savedImages.save()
        return redirect(f"/post/{post.id}")
    return redirect(f"/post/{post.id}")


def unsavePost(request, Id):
    post = Post.objects.get(id=Id)
    UserSavedImage.objects.filter(post=post, user=request.user.id).delete()
    return redirect(f"/post/{post.id}")
