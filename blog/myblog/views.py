import logging

from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from .models import Comment, Post, Tag
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CommentForm, PostForm
from django.shortcuts import render, redirect


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by("-created_on")


class PostDetail(generic.DetailView):
    queryset = Post.objects.all().order_by("-created_on")


class CreatePost(LoginRequiredMixin, generic.CreateView):
    login_url = reverse_lazy("login")
    success_url = reverse_lazy("post_list")

    form_class = PostForm
    queryset = Post.objects.all()
    template_name = "myblog/post_form.html"

    def post(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.POST["author"] = request.user
        request.POST._mutable = False

        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class CreateUser(generic.CreateView):
    success_url = reverse_lazy("post_list")
    form_class = UserCreationForm
    queryset = User.objects.all()
    template_name = "registration/signup.html"


class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    login_url = reverse_lazy("login")

    queryset = Post.objects.all()
    form_class = PostForm

    def get_success_url(self):
        return reverse_lazy(
            "post_detail",
            args=(
                {
                    self.object.id,
                }
            )
        )


class PostDraftList(LoginRequiredMixin, generic.ListView):
    success_url = reverse_lazy("login")
    queryset = Post.objects.filter(status=0).order_by("-created_on")

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)


class PostArchivedList(LoginRequiredMixin, generic.ListView):
    success_url = reverse_lazy("login")
    queryset = Post.objects.filter(status=2).order_by("-created_on")

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)


class PostByTagList(LoginRequiredMixin, generic.ListView):
    success_url = reverse_lazy("login")
    queryset = Post.objects.filter(status=1, tags__id=2).order_by("-created_on")

    def get_queryset(self):
        return super().get_queryset()


class PostDelete(LoginRequiredMixin, generic.DeleteView):
    queryset = Post.objects.all()
    success_url = reverse_lazy("post_list")


@login_required()
def add_comment(request, pk):
    post = Post.objects.filter(pk=pk).first()
    if request.method == "POST":
        request.POST._mutable = True
        request.POST["author"] = request.user
        request.POST["post"] = post
        request.POST._mutable = False
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = CommentForm
    return render(request, "myblog/comment_form.html", {"form": form})

# class AddComment(LoginRequiredMixin, generic.CreateView):
#     queryset = Post.objects.filter(pk=pk).first()
#     form_class = CommentForm
#     template_name = "myblog/comment_form.html"


@login_required
def post_publish(request, pk):
    Post.objects.filter(pk=pk).update(status=1)
    return redirect("post_detail", pk=pk)


@login_required
def post_archive(request, pk):
    Post.objects.filter(pk=pk).update(status=2)
    return redirect("post_detail", pk=pk)