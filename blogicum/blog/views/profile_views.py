from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView

from blog.forms import UserForm
from blog.models import Post, User


class ProfileDetailView(ListView):
    model = Post
    template_name = 'blog/profile.html'
    paginate_by = settings.POSTS_ON_PAGE

    def dispatch(self, request, *args, **kwargs):
        self.profile = get_object_or_404(User, username=kwargs['username'])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Post.posts.filter(author=self.profile)
        if self.profile == self.request.user:
            return queryset.authors_posts()
        else:
            return queryset.visible_posts()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.profile
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email')
    template_name = 'blog/user.html'

    def get_succes_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'pk': self.request.GET.get('pk')})


@login_required
def profile_edit(request):
    form = UserForm(request.POST or None, instance=request.user)
    context = {'form': form}
    if form.is_valid():
        form.save()
        return redirect(
            reverse_lazy('blog:profile',
                         kwargs={'username': request.user.username}))
    return render(request, 'blog/user.html', context)
