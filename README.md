# AI Resume Analyzer

An AI-powered resume analyzer built with Python and Django that compares resumes against job descriptions, calculates an ATS-style match score, identifies missing skills, and generates a downloadable PDF report — deployed live, handling real input.

Live Demo: https://ai-resume-analyzer-elqe.onrender.com

---

## Problem

Most resume-screening tools only measure keyword overlap, with no clear feedback loop for the candidate — you don't know *why* you scored the way you did, or what's actually missing versus what just wasn't phrased the way the system expected.

## Solution

This project parses a resume and a job description, scores their relevance using TF-IDF similarity and cosine similarity, and surfaces the result as an interpretable score with matched and missing skills — not a black-box number — packaged into a downloadable PDF report.

---

## Features

- Upload resumes in PDF and DOCX formats
- Automatic resume text extraction
- Add job description for comparison
- TF-IDF-based similarity scoring between resume and job description
- ATS-style compatibility score
- Matched vs. missing skill detection
- Personalized recommendations based on gaps found
- Downloadable PDF analysis report
- Responsive Bootstrap UI
- PostgreSQL-backed persistence
- Live deployment on Render

---

## Architecture / Workflow

```
Upload resume (PDF/DOCX) → extract & clean text → add job description →
TF-IDF vectorization (resume + job description) → cosine similarity scoring →
rule-based skill matching → combined ATS score → PostgreSQL persistence →
PDF report generation (ReportLab) → served via Django
```

## How the Scoring Works

**TF-IDF (Term Frequency – Inverse Document Frequency):** weighs each word by how often it appears in a given document *and* how rare it is across documents overall — so common filler words contribute little, while distinctive, resume-specific terms carry more weight.

**Cosine similarity:** measures the angle between the resume's and job description's TF-IDF vectors — a score close to 1 means the two documents emphasize similar content, close to 0 means they don't, regardless of document length.

**Skill matching:** runs separately from the similarity score, using rule-based keyword matching to explicitly list matched and missing skills — giving the user actionable detail beyond a single number.

## Known Limitations

TF-IDF is purely frequency-based — it has no semantic understanding. Two resumes phrased differently but meaning the same thing (e.g., "led a team" vs. "managed people") can score as dissimilar even though a human reader would treat them the same. This is a known, understood limitation of the approach, not an oversight.

---

## Tech Stack

- **Backend:** Python, Django
- **Database:** PostgreSQL
- **AI/ML:** Scikit-learn, TF-IDF vectorization, cosine similarity
- **PDF Generation:** ReportLab
- **Frontend:** HTML, CSS, Bootstrap 5
- **Deployment:** Render
- **Other:** Git, GitHub

## Installation

```bash
git clone https://github.com/rumaisemhmd/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration

Set up your PostgreSQL connection details and Django secret key in `.env` or `settings.py` before running migrations. *(Update with your project's actual required environment variables.)*

## How to Run

```bash
python manage.py migrate
python manage.py runserver
```

---

## Future Improvements

- Replace/supplement TF-IDF with sentence embeddings (e.g., Sentence-BERT) for meaning-based matching rather than pure word overlap
- Build a labeled evaluation set (human-scored resume/job-description pairs) to formally measure matching accuracy, rather than relying on informal review
- Introduce a vector database for efficient matching against a large set of job descriptions at once, if scaled beyond one-to-one comparisons

---

## Author

Mohammed Rumaise A
GitHub: https://github.com/rumaisemhmd LinkedIn: https://linkedin.com/in/mohammed-rumaise-a-dev
