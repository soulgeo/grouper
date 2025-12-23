from django.forms import ModelForm

from core.models import Post, PostContent


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title"]


class PostContentForm(ModelForm):
    class Meta:
        model = PostContent
        fields = ["text"]
