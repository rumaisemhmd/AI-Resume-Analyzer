from django import forms
from .models import Resume, JobDescription
from .models import Analysis

class ResumeForm(forms.ModelForm):

    class Meta:
        model = Resume
        fields = ['resume_file']


class JobDescriptionForm(forms.ModelForm):

    class Meta:
        model = JobDescription
        fields = ['title', 'description']

class AnalysisForm(forms.ModelForm):

    class Meta:
        model = Analysis
        fields = ["resume", "job"]

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["resume"].queryset = Resume.objects.filter(user=user)