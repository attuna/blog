from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from .models import Comment, Post
from django.contrib.auth.models import User


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by("-created_on")


class CreateUser(generic.CreateView):
    success_url = reverse_lazy("post_list")
    form_class = UserCreationForm
    queryset = User.objects.all()
    template_name = "registration/signup.html"
