
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("like/<int:post_id>", views.like, name="like"),
    path("follow", views.follow, name="follow"),
    path("users", views.users, name="users"),
    path("users/<int:user_id>", views.user, name="user"),
    path("posts", views.posts, name="posts"),
    path("posts/new", views.new_post, name="new_post"),  
    path("posts/<int:post_id>", views.post, name="post"),
]
