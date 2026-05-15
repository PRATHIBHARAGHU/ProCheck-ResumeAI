from django.contrib import admin
from .models import Resume, JobDescription, AnalysisResult, ExtractedSkill

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('user', 'file', 'uploaded_at')
    search_fields = ('user__username', 'extracted_text')

@admin.register(JobDescription)
class JobDescriptionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    search_fields = ('title', 'content', 'user__username')

class ExtractedSkillInline(admin.TabularInline):
    model = ExtractedSkill
    extra = 0

@admin.register(AnalysisResult)
class AnalysisResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'job_description', 'ats_score', 'created_at')
    list_filter = ('ats_score', 'created_at')
    search_fields = ('user__username', 'job_description__title')
    inlines = [ExtractedSkillInline]