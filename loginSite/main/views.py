from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import RegisterForms, PostForms
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group, Permission
from .models import Post

@login_required(login_url="login")
def home(request):
    posts = Post.objects.all()

    if request.method == 'POST':
        postId = request.POST.get('post-id')
        authorId = request.POST.get('author-id')
        if postId:
            post = Post.objects.filter(id=postId).first()
            if post and (request.user == post.author or request.user.has_perm("main.delete_post")):
                post.delete()
        elif authorId:
            user = User.objects.filter(id=authorId).first()
            if user and request.user.is_staff:
                try:
                    group = Group.objects.get(name="default")
                    group.user_set.remove(user)
                except:
                    pass

                
                try:
                    group = Group.objects.get(name="mod")
                    group.user_set.remove(user)
                except:
                    pass

        return redirect('home')
    return render(request, "main/home.html", {"posts":posts})

def sign_up(request):
    if request.method == "POST":
        form = RegisterForms(request.POST)
        if form.is_valid():
            user = form.save()
            df, created = Group.objects.get_or_create(name="default")
            df.user_set.add(user)
            login(request, user)
            return redirect(reverse('home'))
    else:
        form = RegisterForms()
    return render(request, "registration/sign_up.html", {'form' : form })

@login_required(login_url="login")
@permission_required("main.add_post", login_url="login", raise_exception=True)
def new_post(request):
    if request.method == 'POST':
        form = PostForms(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(reverse("home"))
    else:
        form = PostForms()
    return render(request, "main/new_post.html", {"form":form})

@login_required(login_url="login")
def profile(request):
    posts = Post.objects.filter(author=request.user).all()

    return render(request, 'main/profile.html', {"posts":posts, "author":request.user})


# Create your views here.
