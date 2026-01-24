from django.forms import ModelForm
from .models import ChatRoom

class ChatForm(ModelForm):
    class Meta:
        model = ChatRoom
        fields = ["image", "name"]
