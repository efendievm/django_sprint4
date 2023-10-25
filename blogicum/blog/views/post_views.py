from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from blog.forms import CommentForm, PostForm
from blog.mixins import (
    PostModelMixin, PostRedirectToProfileMixin, PostRedirectToSelfMixin,
    PostsUpdateMixin, PostRedirectToSelfMixin)
from blog.models import Category, Post


class PostListView(PostModelMixin, ListView):
    queryset = Post.published.with_comments()
    template_name = 'blog/list.html'
    paginate_by = settings.POSTS_ON_PAGE


class PostDetailView(PostModelMixin, DetailView):
    template_name = 'blog/detail.html'

    def get_object(self):
        post_id = self.kwargs['pk']
        author_id = get_object_or_404(Post, pk=post_id).author_id
        if (author_id == self.request.user.id):
            return Post.detailed.get(pk=post_id)
        return get_object_or_404(Post.published, pk=post_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments(manager='with_author').all()
        return context


class PostCreatelView(PostsUpdateMixin, PostRedirectToProfileMixin,
                      CreateView):
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostEditView(PostsUpdateMixin, PostRedirectToSelfMixin, UpdateView):
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            return redirect(self.link_to_post())
        return super().dispatch(request, *args, **kwargs)


class PostDeleteView(PostsUpdateMixin, PostRedirectToProfileMixin, DeleteView):
    def dispatch(self, request, *args, **kwargs):
        self.instance = get_object_or_404(Post, pk=kwargs['pk'])
        if self.instance.author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(instance=self.instance)
        return context


class CategoryListView(PostModelMixin, ListView):
    template_name = 'blog/category.html'
    paginate_by = settings.POSTS_ON_PAGE

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(
            Category, slug=kwargs['category_slug'], is_published=True)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.category.posts(
            manager='published').with_comments()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context
