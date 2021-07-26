from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, response
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

import json

from .models import User, Post, Comment, Following

def index(request):
    # Authenticated users view the page
    if request.user.is_authenticated:
        # Filter emails returned based on mailbox
        posts = Post.objects.all()
        context = {'posts': posts}
        return render(request, "network/index.html", context)

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))

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

@csrf_exempt
@login_required
def new_post(request):
    # Composing a new email must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Get contents of the post
    data = json.loads(request.body)
    body = data.get("body", "")
    
    # Check content
    if body == "":
        return JsonResponse({
            "error": "Please add some content."
        }, status=400)

    # Create the post
    post = Post(
        author = request.user,
        text = body
    )
    post.save()

    return JsonResponse({"message": "Post sent successfully."}, status=201)

@login_required
def users(request):

    # Query for users
    users = User.objects.all
    user = User.objects.get(pk=request.user.id)
    following = user.following.all()
    followingList = []
    for follow in following:
        followingList.append(follow.following)

    # Return user profile
    if request.method == "GET":
        return render(request, "network/users.html", {'users': users, 'following': followingList})


@login_required
def follow(request):

    # Return user profile
    if request.method == "POST":
        # Query for users
        user = User.objects.get(pk=request.user.id)
        following = user.following.all()
        user_follow_id = request.POST.get('follow')
        user_follow = User.objects.get(pk=user_follow_id)

        if following.filter(following__username=user_follow.username):
            follow = following.filter(following__username=user_follow.username)
            follow.delete()
        else:
            follow = Following.objects.create(user=user, following=user_follow)
            follow.save()
        print(request.path_info)
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@login_required
def following(request):
    # Filter emails returned based on mailbox
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, "network/index.html", context)


@login_required
def user(request, user_id):

    try:
        user = User.objects.get(pk=user_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)
    
    followers = user.followers.all()
    followersList = []
    for follow in followers:
        followersList.append(follow.user)

    # Return user profile
    return render(request, "network/user.html", {'user_network': user, 'followers': followersList})

@csrf_exempt
@login_required
def post(request, post_id):

    # Query for requested
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Return contents
    if request.method == "GET":
        return render(request, "network/post.html", {'post': post})
    elif request.method == "POST":
        if request.user not in post.likes.all():
            post.likes.add(request.user)
        else:
            post.likes.remove(request.user)
        post.save()
        return render(request, "network/post.html", {'post': post})

    # Update whether email is read or should be archived
    elif request.method == "PUT":
        if request.user not in post.likes.all():
            post.likes.add(request.user)
        else:
            post.likes.remove(request.user)
        post.save()
        response = JsonResponse({"status": "Like updated.", "nbLikes": post.number_of_likes()})
        return response
