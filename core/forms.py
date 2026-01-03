from django.forms import ModelForm

from core.models import Post, PostContent
from users.models import User, UserProfile


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title", "visibility"]


class PostContentForm(ModelForm):
    class Meta:
        model = PostContent
        fields = ["text"]


class UserSearchForm(ModelForm):
    class Meta:
        model = User
        fields = ["username"]


class UserProfileSearchForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ["country", "interests"]
