from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={
                'style': 'width: 100%; padding: 0.5rem; border-radius: 0.375rem; border: 1px solid var(--border-color);'
            }),
            'comment': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Share your experience with this provider...',
                'style': 'width: 100%; padding: 0.5rem; border-radius: 0.375rem; border: 1px solid var(--border-color); resize: vertical;'
            }),
        }
