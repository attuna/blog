from django.urls import path
from . import views

urlpatterns = [
    path("", views.PostList.as_view(), name="post_list"),
    path("user/new/", views.CreateUser.as_view(), name="new_user"),
    path("post/new", views.CreatePost.as_view(), name="post_new"),
    path("post/<int:pk>/", views.PostDetail.as_view(), name="post_detail"),
    path("post/<int:pk>/edit/", views.PostUpdateView.as_view(), name="post_update"),


]
