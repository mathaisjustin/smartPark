from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):

   class Meta:
      model = Feedback
      fields = ['name', 'email','message', 'image']