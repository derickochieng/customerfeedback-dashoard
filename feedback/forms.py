from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['source']  # We do not include 'showroom' because it is auto-assigned.
