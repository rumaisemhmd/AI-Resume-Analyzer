import os

from django import forms

ALLOWED_RESUME_EXTENSIONS = {".pdf", ".docx"}


class AnalyzeUploadForm(forms.Form):

    resume_file = forms.FileField(
        label="Resume",
        widget=forms.ClearableFileInput(attrs={"accept": ".pdf,.docx"}),
    )

    job_title = forms.CharField(
        label="Job title",
        max_length=200,
        widget=forms.TextInput(attrs={"placeholder": "e.g. Senior Backend Engineer"}),
    )

    job_description = forms.CharField(
        label="Job description",
        widget=forms.Textarea(attrs={
            "rows": 8,
            "placeholder": "Paste the full job description here...",
        }),
    )

    def clean_resume_file(self):
        resume_file = self.cleaned_data["resume_file"]
        extension = os.path.splitext(resume_file.name)[1].lower()
        if extension not in ALLOWED_RESUME_EXTENSIONS:
            raise forms.ValidationError("Upload a .pdf or .docx file.")
        return resume_file
