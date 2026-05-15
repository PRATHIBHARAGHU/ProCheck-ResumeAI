from django.db import models
from django.contrib.auth.models import User
import json

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    file = models.FileField(upload_to='resumes/%Y/%m/%d/')
    extracted_text = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Resume ({self.uploaded_at.strftime('%Y-%m-%d')})"

class JobDescription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_descriptions')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class AnalysisResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='analyses')
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='analyses')
    job_description = models.ForeignKey(JobDescription, on_delete=models.CASCADE, related_name='analyses')
    
    ats_score = models.IntegerField()
    keyword_score = models.IntegerField()
    semantic_score = models.IntegerField()
    skills_score = models.IntegerField()
    formatting_score = models.IntegerField()
    
    matched_skills = models.TextField()  # JSON-serialized array
    missing_skills = models.TextField()  # JSON-serialized array
    suggestions = models.TextField()      # JSON-serialized array
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def set_matched_skills(self, x): self.matched_skills = json.dumps(x)
    def get_matched_skills(self): return json.loads(self.matched_skills) if self.matched_skills else []
    
    def set_missing_skills(self, x): self.missing_skills = json.dumps(x)
    def get_missing_skills(self): return json.loads(self.missing_skills) if self.missing_skills else []
    
    def set_suggestions(self, x): self.suggestions = json.dumps(x)
    def get_suggestions(self): return json.loads(self.suggestions) if self.suggestions else []

class ExtractedSkill(models.Model):
    analysis = models.ForeignKey(AnalysisResult, on_delete=models.CASCADE, related_name='extracted_skills_list')
    skill_name = models.CharField(max_length=100)
    skill_type = models.CharField(max_length=50) # e.g. language, framework, database

    def __str__(self):
        return f"{self.skill_name} ({self.skill_type})"