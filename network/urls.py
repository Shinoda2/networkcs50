
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path('follow/', views.follow),

    # API Routes
    path("likes", views.likeposts, name="likeposts"),
    path("edit_post", views.edit_post, name="editpost"),

]
