import os
from django.shortcuts import render, redirect
from .forms import ResumeForm
from .resume_parser.pdf_parser import extract_pdf_text
from .resume_parser.docx_parser import extract_docx_text
from .forms import JobDescriptionForm
from .models import Analysis
from .forms import AnalysisForm
from .ai_engine.similarity_engine import (calculate_similarity, calculate_final_score)
from .ai_engine.skill_extractor import (extract_skills,matched_skills,missing_skills)
from .models import Analysis
from .ai_engine.recommendation import generate_recommendation
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph 
from reportlab.lib.styles import getSampleStyleSheet

def home(request):
    return render(request, "home.html")


def upload_resume(request):

    if request.method == "POST":

        form = ResumeForm(request.POST, request.FILES)

        if form.is_valid():
            resume = form.save()

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
            return redirect("upload_resume")

    else:
        form = ResumeForm()

    return render(
        request,
        "upload_resume.html",
        {"form": form}
    )

def job_description(request):

    if request.method == "POST":

        form = JobDescriptionForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("job_description")

    else:
        form = JobDescriptionForm()

    return render(
        request,
        "job_description.html",
        {"form": form}
    )

def analyze_resume(request):

    if request.method == "POST":

        form = AnalysisForm(request.POST)

        if form.is_valid():

            analysis = form.save(commit=False)

            resume = analysis.resume
            job = analysis.job

          
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
            analysis.similarity_score = score
            analysis.matched_skills = ", ".join(matched)
            analysis.missing_skills = ", ".join(missing)

            analysis.save()

            return redirect("analysis_result", analysis.id)

    else:
        form = AnalysisForm()

    return render(request, "analyze.html", {"form": form})

def analysis_result(request, analysis_id):

    analysis = Analysis.objects.get(id=analysis_id)

    matched = []

    if analysis.matched_skills:
        matched = analysis.matched_skills.split(",")

    missing = []

    if analysis.missing_skills:
        missing = analysis.missing_skills.split(",")

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
    
def dashboard(request):

    analyses = Analysis.objects.all().order_by("-created_at")

    return render(
        request,
        "dashboard.html",
        {
            "analyses": analyses
        }
    )
def download_report(request, analysis_id):

    analysis = Analysis.objects.get(id=analysis_id)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        'attachment; filename="analysis_report.pdf"'
    )

    document = SimpleDocTemplate(response)

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>AI Resume Analyzer Report</b>", styles["Title"]))

    story.append(Paragraph(f"<b>Resume:</b> {analysis.resume.resume_file.name}", styles["BodyText"]))

    story.append(Paragraph(f"<b>Job:</b> {analysis.job.title}", styles["BodyText"]))

    story.append(Paragraph(f"<b>Match Score:</b> {analysis.similarity_score:.2f}%", styles["BodyText"]))

    story.append(Paragraph(f"<b>Matched Skills:</b> {analysis.matched_skills}", styles["BodyText"]))

    story.append(Paragraph(f"<b>Missing Skills:</b> {analysis.missing_skills}", styles["BodyText"]))

    recommendation = generate_recommendation(
        analysis.similarity_score,
        analysis.missing_skills
    )

    story.append(Paragraph(f"<b>Recommendation:</b> {recommendation}", styles["BodyText"]))

    document.build(story)

    return response