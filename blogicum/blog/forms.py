from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q

from .models import Category, Comment, Location, Post, User


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'] = forms.ModelChoiceField(
            queryset=Category.objects.filter(is_published=True))
        self.fields['location'] = forms.ModelChoiceField(
            queryset=Location.objects.filter(is_published=True))

    class Meta:
        model = Post
        fields = (
            'title', 'text', 'pub_date', 'location', 'category', 'image',
        )
        widgets = {
            'pub_date': forms.DateInput(format=('%Y-%m-%d'),
                                        attrs={'type': 'date'})
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class UserForm(forms.ModelForm):
    def clean_email(self):
        email = self.data['email']
        username = self.data['username']
        if (self.data['email']
            and User.objects.filter(
                ~Q(username=username) & Q(email=email)).exists()):
            raise ValidationError(
                'Пользователь с указанным email зарагестрирован'
            )
        return email

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',)
