from django.forms import ModelForm
from core.models import Room


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = "__all__"
