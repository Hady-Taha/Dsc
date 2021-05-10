from django import forms
from .models import Comments
class CreateComment(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('content',)