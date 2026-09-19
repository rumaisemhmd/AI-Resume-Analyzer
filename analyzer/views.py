import os
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .forms import AnalyzeUploadForm
from .resume_parser.pdf_parser import extract_pdf_text
from .resume_parser.docx_parser import extract_docx_text
from .models import Analysis, JobDescription, Resume
from .ai_engine.similarity_engine import (calculate_similarity, calculate_final_score)
from .ai_engine.skill_extractor import (extract_skills,matched_skills,missing_skills)
from .ai_engine.recommendation import generate_recommendation
from django.http import HttpResponse, HttpResponseForbidden
from .reports import build_analysis_report

def home(request):
    return render(request, "home.html")


@login_required
def analyze_resume(request):

    if request.method == "POST":

        form = AnalyzeUploadForm(request.POST, request.FILES)

        if form.is_valid():

            resume = Resume.objects.create(
                user=request.user,
                resume_file=form.cleaned_data["resume_file"],
            )

            file_path = resume.resume_file.path
            extension = os.path.splitext(file_path)[1].lower()

            if extension == ".pdf":
                text = extract_pdf_text(file_path)
            elif extension == ".docx":
                text = extract_docx_text(file_path)
            else:
                text = ""

            resume.extracted_text = text
            resume.save()

            job = JobDescription.objects.create(
                title=form.cleaned_data["job_title"],
                description=form.cleaned_data["job_description"],
            )

            tfidf_score = calculate_similarity(
                resume.extracted_text,
                job.description
            )

            resume_skill_list = extract_skills(resume.extracted_text)
            job_skill_list = extract_skills(job.description)

            matched = matched_skills(
                resume_skill_list,
                job_skill_list
            )

            missing = missing_skills(
                resume_skill_list,
                job_skill_list
            )
            score = calculate_final_score(
                tfidf_score,
                len(matched),
                len(job_skill_list)
            )

            analysis = Analysis.objects.create(
                user=request.user,
                resume=resume,
                job=job,
                similarity_score=score,
                matched_skills=", ".join(matched),
                missing_skills=", ".join(missing),
            )

            return redirect("analysis_result", analysis.id)

    else:
        form = AnalyzeUploadForm()

    return render(request, "analyze.html", {"form": form})

@login_required
def analysis_result(request, analysis_id):

    analysis = get_object_or_404(Analysis, id=analysis_id)

    if analysis.user_id != request.user.id:
        return HttpResponseForbidden("You do not have access to this analysis.")

    matched = []

    if analysis.matched_skills:
        matched = [skill.strip() for skill in analysis.matched_skills.split(",")]

    missing = []

    if analysis.missing_skills:
        missing = [skill.strip() for skill in analysis.missing_skills.split(",")]

    recommendation = generate_recommendation(
        analysis.similarity_score,
        analysis.missing_skills
    )

    return render(
        request,
        "analysis_result.html",
        {
            "analysis": analysis,
            "matched": matched,
            "missing": missing,
            "recommendation": recommendation,
        }
    )

@login_required
def dashboard(request):

    analyses = Analysis.objects.filter(user=request.user).order_by("-created_at")

    return render(
        request,
        "dashboard.html",
        {
            "analyses": analyses
        }
    )

@login_required
def download_report(request, analysis_id):

    analysis = get_object_or_404(Analysis, id=analysis_id)

    if analysis.user_id != request.user.id:
        return HttpResponseForbidden("You do not have access to this analysis.")

    matched = []

    if analysis.matched_skills:
        matched = [skill.strip() for skill in analysis.matched_skills.split(",")]

    missing = []

    if analysis.missing_skills:
        missing = [skill.strip() for skill in analysis.missing_skills.split(",")]

    recommendation = generate_recommendation(
        analysis.similarity_score,
        analysis.missing_skills
    )

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        'attachment; filename="analysis_report.pdf"'
    )

    build_analysis_report(response, analysis, matched, missing, recommendation)

    return response
