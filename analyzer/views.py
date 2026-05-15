from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.files.storage import FileSystemStorage
from .models import Resume, JobDescription, AnalysisResult, ExtractedSkill
from .services.pdf_parser import PDFParserService
from .services.ats_engine import ATSScoringEngine
import json

class LandingPageView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('analyzer:dashboard')
        return render(request, 'landing.html')

class AboutPageView(View):
    def get(self, request):
        return render(request, 'analyzer/about.html')

class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        analyses = AnalysisResult.objects.filter(user=request.user).order_by('-created_at')
        total_analyzed = analyses.count()
        
        avg_score = 0
        if total_analyzed > 0:
            avg_score = int(sum([a.ats_score for a in analyses]) / total_analyzed)
            
        recent_activity = analyses[:5]
        
        # Build metrics array for Chart.js dashboard integration tracking stream
        chart_labels = [a.created_at.strftime('%m/%d') for a in reversed(analyses[:7])]
        chart_data = [a.ats_score for a in reversed(analyses[:7])]

        context = {
            'total_analyzed': total_analyzed,
            'avg_score': avg_score,
            'recent_activity': recent_activity,
            'chart_labels': json.dumps(chart_labels),
            'chart_data': json.dumps(chart_data)
        }
        return render(request, 'analyzer/dashboard.html', context)

class AnalyzeResumeView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'analyzer/analyze.html')

    def post(self, request):
        jd_title = request.POST.get('job_title')
        jd_content = request.POST.get('job_description')
        resume_file = request.FILES.get('resume_file')

        if not jd_title or not jd_content or not resume_file:
            messages.error(request, "All validation input fields are mandatory parameters.")
            return redirect('analyzer:analyze')

        if not resume_file.name.endswith('.pdf'):
            messages.error(request, "Invalid structural validation mapping: Resume must be PDF format.")
            return redirect('analyzer:analyze')

        try:
            # 1. Parse operational textual corpus
            extracted_text = PDFParserService.extract_text(resume_file)
            if not extracted_text.strip():
                messages.error(request, "Failed to extract valid text from the PDF file. Ensure it is not scanned/an image.")
                return redirect('analyzer:analyze')

            # 2. Persist tracking model entities
            resume_obj = Resume.objects.create(user=request.user, file=resume_file, extracted_text=extracted_text)
            jd_obj = JobDescription.objects.create(user=request.user, title=jd_title, content=jd_content)

            # 3. Analyze text with NLP engine
            engine = ATSScoringEngine()
            metrics = engine.analyze(extracted_text, jd_content)

            # 4. Persist analysis results
            result = AnalysisResult(
                user=request.user,
                resume=resume_obj,
                job_description=jd_obj,
                ats_score=metrics['final_score'],
                keyword_score=metrics['keyword_score'],
                semantic_score=metrics['semantic_score'],
                skills_score=metrics['skills_score'],
                formatting_score=metrics['formatting_score']
            )
            result.set_matched_skills(metrics['matched_skills'])
            result.set_missing_skills(metrics['missing_skills'])
            result.set_suggestions(metrics['suggestions'])
            result.save()

            # 5. Populate relational granular skill categorization matrices
            for category, skill_list in metrics['categorized_resume_skills'].items():
                for skill_name in skill_list:
                    ExtractedSkill.objects.create(analysis=result, skill_name=skill_name, skill_type=category)

            messages.success(request, "Advanced algorithmic parsing sequence completed.")
            return redirect('analyzer:report', pk=result.pk)

        except Exception as e:
            messages.error(request, f"Processing execution failure context: {str(e)}")
            return redirect('analyzer:analyze')

class AnalysisReportView(LoginRequiredMixin, View):
    def get(self, request, pk):
        report = get_object_or_404(AnalysisResult, pk=pk, user=request.user)
        context = {
            'report': report,
            'matched_skills': report.get_matched_skills(),
            'missing_skills': report.get_missing_skills(),
            'suggestions': report.get_suggestions(),
            'categorized_skills': report.extracted_skills_list.all()
        }
        return render(request, 'analyzer/report.html', context)

class ExportReportPDFView(LoginRequiredMixin, View):
    def get(self, request, pk):
        report = get_object_or_404(AnalysisResult, pk=pk, user=request.user)
        # Structural fallback JSON data print to stream for standalone headless portability printing
        response = HttpResponse(content_type='application/json')
        response['Content-Disposition'] = f'attachment; filename="ats_report_{report.pk}.json"'
        
        data_packet = {
            "system_label": "Smart Resume Analyzer Report Structural Output Engine",
            "score": report.ats_score,
            "breakdown": {
                "keyword": report.keyword_score,
                "semantic": report.semantic_score,
                "skills": report.skills_score,
                "formatting": report.formatting_score
            },
            "job_title": report.job_description.title,
            "matched_skills": report.get_matched_skills(),
            "missing_skills": report.get_missing_skills(),
            "suggestions": report.get_suggestions()
        }
        response.write(json.dumps(data_packet, indent=4))
        return response

class HistoryView(LoginRequiredMixin, View):
    def get(self, request):
        history = AnalysisResult.objects.filter(user=request.user).order_by('-created_at')
        return render(request, 'analyzer/history.html', {'history': history})

class DeleteReportView(LoginRequiredMixin, View):
    def post(self, request, pk):
        report = get_object_or_404(AnalysisResult, pk=pk, user=request.user)
        report.delete()
        messages.success(request, "Analysis logs permanently removed from database storage.")
        return redirect('analyzer:history')