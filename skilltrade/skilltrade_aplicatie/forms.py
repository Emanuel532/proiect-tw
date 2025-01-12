from django import forms
from .models import Request

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Add a message (optional)...',
                'rows': 3
            }),
        }