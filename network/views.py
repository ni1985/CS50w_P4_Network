from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Post, Follow, PostForm


def index(request):
    
    # create a new post
    if request.method == "POST":
        new_post = PostForm(request.POST)

        if new_post.is_valid():
            post = new_post.save(commit=False)
            post.creator = request.user
            post.save()
    
        return HttpResponseRedirect(reverse('index'))

    else:
        # prepare a form for the new post
        new_post_form = PostForm()

        # retrieve all posts
        posts = Post.objects.select_related('creator').order_by('-post_time')
        #print(posts)
        #print(posts.query)

        return render(request, "network/index.html", {
            'new_post':new_post_form,
            'posts':posts
        })


def profile(request, user_name):
    if request.method == "POST":
        print("post")
    else:
        
        # Check if user opens their own profile
        if (str(request.user) == user_name):
            user_check = 1
            print("same user")
        else: 
            user_check = 0
        print(f"User check: {user_check}")

        user_post = Post.objects.filter(creator__username = user_name).order_by('-post_time')
        
        # Get number of followers
        followed = Follow.objects.filter(subscribed__username = user_name)    
        followed_users = followed.values_list('user_id__username', flat=True)
        followed_nr = len(followed_users)
        print(followed_users)
        print(followed_nr)
        print(f"followed by: {followed_nr}")
        
        # Get number of users followed by the user
        follows = Follow.objects.filter(user_id__username = user_name)
        follows_users = follows.values_list('subscribed__username', flat=True)
        follows_nr = len(follows_users)
        print(follows_users)
        print(follows_nr)
        print(f"follows: {follows_nr}")

        return render(request, "network/profile.html", {
                'user_name': user_name,
                'posts': user_post,
                'follows_nr': follows_nr,
                'followed_nr': followed_nr,
                'user_check': user_check
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
