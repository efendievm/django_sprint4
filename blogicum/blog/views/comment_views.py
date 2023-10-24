from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from blog.mixins import CommentAuthorizedMixin, CommentMixin


class CommentCreateView(CommentMixin, CreateView):
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['post_pk']
        return super().form_valid(form)


class CommentEditView(CommentAuthorizedMixin, UpdateView):
    pass


class CommentDeleteView(CommentAuthorizedMixin, DeleteView):
    def get_success_url(self):
        return reverse_lazy('blog:post_detail',
                            kwargs={'pk': self.kwargs['post_pk']})
