from django import forms
from .models import Assignment, Submission, PeerReview

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = '__all__'

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = '__all__'

class ReviewForm(forms.ModelForm):
    class Meta:
        model = PeerReview
        fields = '__all__'