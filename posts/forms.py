from django import forms

from .models import *


class PostForm(forms.ModelForm):
    class Meta:
        model = Post

        fields = ('content', )
        labels = {
                  "content": "Post content",
                  }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment

        fields = ('content', )
        labels = {
                  "content": "Post content",
                  }
