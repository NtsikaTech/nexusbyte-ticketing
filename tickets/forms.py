# forms.py
from django import forms
from .models import Ticket

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description']
        
    def clean_title(self):
        title = self.cleaned_data['title']
        # Ensure title doesn't contain malicious content
        return title.strip()  # Example of sanitization
