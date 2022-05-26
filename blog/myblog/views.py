from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from .models import Comment, Post
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CommentForm,PostForm


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
            args =(
                {
                    self.object.id,
                }
            )
        )

