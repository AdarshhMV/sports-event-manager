from django import forms
from .models import Registration

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        # Removed 'is_team_member' so students cannot select themselves
        fields = ['sport', 'branch', 'year', 'past_experience', 'certificates']
        
        widgets = {
            'sport': forms.Select(attrs={'class': 'custom-select'}),
            'branch': forms.TextInput(attrs={'placeholder': 'e.g., Computer Science'}),
            'year': forms.Select(attrs={'class': 'custom-select'}),
            'past_experience': forms.Textarea(attrs={
                'rows': 3, 
                'placeholder': 'Briefly describe your past experience (if any)...'
            }),
            'certificates': forms.FileInput(attrs={'class': 'custom-file'}),
        }