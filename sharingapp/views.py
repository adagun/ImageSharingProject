from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.forms import UserProfilePicForm
from accounts.models import UserProfilePicture
from .models import Post, UserFollow, UserSavedImage
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.db.models import Q
from .forms import PostForm
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator



# Create your views here.

def indexView(request):
    return render(request, "index.html")


class PostsView(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = "posts"
    template_name = "posts/posts.html"
    paginate_by = 10
    extra_context={
        'profilePic': UserProfilePicture.objects.order_by("?"),
    }

    def get_context_data(self, **kwargs):
        context = super(PostsView, self).get_context_data(**kwargs)
        user = self.request.user
        followed_user_ids= UserFollow.objects.filter(user=user).values_list('followed_user', flat=True)
        
        idList=list(followed_user_ids)

        unfollowed_users=User.objects.exclude(id__in=idList)  
        unfollowed_users=unfollowed_users.exclude(id = user.id).order_by("?")[:4]
        
        context.update({
        'profilePic': UserProfilePicture.objects.all(),
        'unfollowed_users':unfollowed_users
    })
        return context


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
    postImages = Post.objects.filter(user=request.user).order_by('-uploaded')
    profilePic = UserProfilePicture.objects.filter(user=request.user)

    followers = UserFollow.objects.filter(followed_user=request.user).count()
    followeing = UserFollow.objects.filter(user=request.user).count()


    context = {
        "postImages": postImages,
        "profilePic": profilePic,
        "followers": followers,
        "followeing": followeing,
        "picId": profilePic.first().id
    }
    return render(request, "profile.html", context)


@login_required
def savedPostsView(request):
    savedImages = UserSavedImage.objects.filter(user=request.user).order_by('-post__uploaded')
    profilePic = UserProfilePicture.objects.filter(user=request.user)

    postImages = Post.objects.filter(user=request.user)
    followers = UserFollow.objects.filter(followed_user=request.user).count()
    followeing = UserFollow.objects.filter(user=request.user).count()

    context = {
        "savedImages": savedImages,
        "postImages": postImages,
        "profilePic": profilePic,
        "followers": followers,
        "followeing": followeing,
        "picId": profilePic.first().id,

    }
    return render(request, "profile.html", context)


def userPage(request, Id):
    postImages = Post.objects.filter(user=Id)
    user = User.objects.get(id=Id)
    userFollow = UserFollow.objects.filter(user=request.user, followed_user=user)
    profilePic = UserProfilePicture.objects.filter(user=user)


    followers = UserFollow.objects.filter(followed_user=request.user).count()
    followeing = UserFollow.objects.filter(user=request.user).count()

    if userFollow:
        exists = True
    else:
        exists = False
    context = {
        "currentUser": user,
        "postImages": postImages,
        "exists": exists,
        "profilePic": profilePic,
        "followers": followers,
        "followeing": followeing
    }
    return render(request, "userPage.html", context)


class PostView(LoginRequiredMixin, DetailView):
    model = Post
    context_object_name = "post"
    template_name = "posts/post.html"

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        user_saved_set = self.request.user.usersavedimage_set.all().values_list('post', flat=True)
        if context["object"].id in user_saved_set:
            context['user_has_saved'] = True

        return context


def searchbar(request):

    if request.method == 'GET':
        query = request.GET.get('q')
        submitbutton = request.GET.get('submit')

        if query is not None:
            lookups = Q(title__icontains=query) | Q(description__icontains=query) | Q(user__username__icontains=query)
            results = Post.objects.filter(lookups).distinct()
            profilePic = UserProfilePicture.objects.all()

            followed_user_ids= UserFollow.objects.filter(user=request.user).values_list('followed_user', flat=True)
        
            idList=list(followed_user_ids)
            
            unfollowed_users=User.objects.exclude(id__in=idList)  
            unfollowed_users=unfollowed_users.exclude(id = request.user.id)[:4]

            context = {
                'results': results, 'submitbutton': submitbutton,
                "profilePic":profilePic,
                'unfollowed_users':unfollowed_users
                }

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
        savedImages.user = request.user
        savedImages.post = post
        savedImages.save()
        return redirect(f"/post/{post.id}")
    return redirect(f"/post/{post.id}")


def followUser(request, Id):
    user = User.objects.get(id=Id)
    followed = UserFollow()
    exists = UserFollow.objects.filter(followed_user=user, user=request.user)
    if not exists:
        followed.user = request.user
        followed.followed_user = user
        followed.save()
        return redirect(f"/userPage/{user.id}")
    return redirect(f"/userPage/{user.id}")


def deleteFollowUser(request, Id):
    user = User.objects.get(id=Id)
    followed = UserFollow.objects.filter(followed_user=user, user=request.user).delete()
    return redirect(f"/userPage/{user.id}")


@login_required
def followedUserPage(request):
    followed = UserFollow.objects.filter(user=request.user)
    n = 1
    posts1=[]
    posts2=[]
    posts3=[]
    posts4=[]
    for f in followed:
        postsObj = Post.objects.filter(user = f.followed_user).order_by('-uploaded')
        for p in postsObj:
            if n == 1 :
                posts1.append(p)
                n = n + 1
            elif n == 2 :
                posts2.append(p)
                n = n + 1
            elif n == 3 :
                posts3.append(p)
                n = n + 1
            else:
                posts4.append(p)
                n = 1

    context = {
        "posts1":posts1,
        "posts2":posts2,
        "posts3":posts3,
        "posts4":posts4,
        
        }         
    return render(request, "followed_user_page.html", context)


def unsavePost(request, Id):
    post = Post.objects.get(id=Id)
    UserSavedImage.objects.filter(post=post, user=request.user.id).delete()
    return redirect(f"/post/{post.id}")


class EditProfilePicture(UserPassesTestMixin, UpdateView):
    # prevent other users from accessing other users edit profile picture page
    def test_func(self):
        profilePic = UserProfilePicture.objects.filter(user=self.request.user).first()
        return profilePic.id == self.get_object().id
    model = UserProfilePicture
    form_class = UserProfilePicForm
    success_url = reverse_lazy('profile')
    template_name = "profile_pic_form.html"