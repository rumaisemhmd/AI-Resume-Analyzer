from django.db import models

class Resume(models.Model):

    resume_file = models.FileField(upload_to="resumes/")

    extracted_text = models.TextField(blank=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.resume_file.name
    
class JobDescription(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.title
    
class Analysis(models.Model):

    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE
    )

    job = models.ForeignKey(
        JobDescription,
        on_delete=models.CASCADE
    )

    similarity_score = models.FloatField()

    matched_skills = models.TextField(blank=True)

    missing_skills = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.resume} - {self.similarity_score}%"