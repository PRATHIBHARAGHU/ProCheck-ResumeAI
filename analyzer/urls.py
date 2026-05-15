from django.urls import path
from .views import (
    DashboardView, AnalyzeResumeView, AnalysisReportView, 
    HistoryView, DeleteReportView, ExportReportPDFView
)

app_name = 'analyzer'

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('analyze/', AnalyzeResumeView.as_view(), name='analyze'),
    path('report/<int:pk>/', AnalysisReportView.as_view(), name='report'),
    path('report/<int:pk>/export/', ExportReportPDFView.as_view(), name='export'),
    path('history/', HistoryView.as_view(), name='history'),
    path('report/<int:pk>/delete/', DeleteReportView.as_view(), name='delete'),
]