
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:owner>", views.profile, name="profile"),

    # API Routes
    path("posts", views.posts, name="posts"),
    path("posts/<int:post_id>", views.reload_post, name="reload"),
    path("edit_post/<int:post_id>", views.edit_post, name="edit"),
    path("UserRelationship/<str:owner>", views.UserRelationship, name="follow"),
    path("followers/<str:owner>", views.FollowerCount, name="count")

    # # API Routes
    # path("emails", views.compose, name="compose"),
    # path("emails/<int:email_id>", views.email, name="email"),
    # path("emails/<str:mailbox>", views.mailbox, name="mailbox"),
]
