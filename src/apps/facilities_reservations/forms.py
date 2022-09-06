from django import forms
from .models import Room, Reservation


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
