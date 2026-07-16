from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("upload/", views.upload_resume, name="upload_resume"),
    path("job/", views.job_description, name="job_description"),
    path("analyze/",views.analyze_resume,name="analyze_resume"),
    path("result/<int:analysis_id>/",views.analysis_result,name="analysis_result"),
    path("dashboard/",views.dashboard,name="dashboard"),
    path("download/<int:analysis_id>/",views.download_report,name="download_report"),
]