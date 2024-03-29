
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:user_name>/", views.profile, name="profile"),
    path("favorites", views.favorites, name="favorites"),

    # API Routes
    path("update-post-text", views.update_post, name="update-post"),
    path("update-post-like", views.update_like, name="update-like"),
]
