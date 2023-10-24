from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from blog.forms import CommentForm, PostForm
from blog.models import Comment, Post


class PostModelMixin:
    model = Post


class PostsUpdateMixin(PostModelMixin, LoginRequiredMixin):
    template_name = 'blog/create.html'
    form_class = PostForm


class PostRedirectToSelfMixin():
    def link_to_post(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'pk': self.get_object().pk})

    def get_success_url(self):
        return self.link_to_post()


class PostRedirectToProfileMixin():
    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username})


class CommentMixin(LoginRequiredMixin):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(Post, pk=kwargs['post_pk'])
        return super().dispatch(request, *args, **kwargs)


class CommentAuthorizedMixin(CommentMixin):
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
