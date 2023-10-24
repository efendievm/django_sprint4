from django.urls import path

from blog.views import comment_views, post_views, profile_views

app_name = 'blog'

urlpatterns = [
    path('',
         post_views.PostListView.as_view(),
         name='index'),
    path('category/<slug:category_slug>/',
         post_views.CategoryListView.as_view(),
         name='category_posts'),
    path('posts/<int:pk>/',
         post_views.PostDetailView.as_view(),
         name='post_detail'),
    path('posts/create/',
         post_views.PostCreatelView.as_view(),
         name='create_post'),
    path('posts/<int:pk>/edit/',
         post_views.PostEditView.as_view(),
         name='edit_post'),
    path('posts/<int:pk>/delete/',
         post_views.PostDeleteView.as_view(),
         name='delete_post'),
    path('posts/<int:post_pk>/comment/',
         comment_views.CommentCreateView.as_view(),
         name='add_comment'),
    path('posts/<int:post_pk>/edit_comment/<int:pk>/',
         comment_views.CommentEditView.as_view(),
         name='edit_comment'),
    path('posts/<int:post_pk>/delete_comment/<int:pk>/',
         comment_views.CommentDeleteView.as_view(),
         name='delete_comment'),
    path('profile/<slug:username>/',
         profile_views.ProfileDetailView.as_view(),
         name='profile'),
    path('profile_edit/',
         profile_views.profile_edit,
         name='edit_profile')
]
