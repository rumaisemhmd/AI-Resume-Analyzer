# AI Resume Analyzer

An AI-powered resume analyzer built with Django that scores a resume against a job description using TF-IDF and cosine similarity, lists exactly which required skills matched and which are missing, and generates a downloadable PDF report — scoped to tech/IT roles, with Google-only sign-in and per-user data isolation.

**Live Demo:** https://ai-resume-analyzer-elqe.onrender.com

This is a portfolio project.

---

## What it does

Upload a resume (PDF or DOCX) and paste in a job description, and AI Resume Analyzer extracts the resume text, vectorizes both documents with TF-IDF, scores their similarity with cosine similarity, and separately runs rule-based keyword matching against a dictionary of tech/IT skills (languages, frameworks, cloud/DevOps, AI/ML, auth, testing, and general SDLC terms) to report matched vs. missing skills. Every result is saved to a private dashboard tied to your Google account and can be exported as a PDF report.

## Tech Stack

- **Backend:** Python, Django
- **Database:** PostgreSQL
- **AI/ML:** scikit-learn (TF-IDF vectorization, cosine similarity)
- **PDF Generation:** ReportLab
- **Auth:** Google OAuth2 via django-allauth (sign-in only, no local passwords)
- **Frontend:** Django templates, Tailwind CSS (CDN, no build step), minimal vanilla JS
- **Deployment:** Render

## Key Features

- Resume/job-description matching via TF-IDF + cosine similarity, producing an interpretable ATS-style score
- Skill matching (matched vs. missing) against a dictionary scoped to tech/IT roles — programming languages, frameworks, cloud/DevOps, AI/ML, auth/security, and testing tools
- Downloadable PDF report per analysis
- Google-only authentication with per-user data isolation — every upload, analysis, and result is scoped to the signed-in account; nothing is visible to other users or to anonymous visitors
- Responsive UI with an animated pipeline diagram showing the actual scoring flow

## How the Scoring Works

**TF-IDF (Term Frequency – Inverse Document Frequency):** weighs each word by how often it appears in a given document *and* how rare it is across documents overall — so common filler words contribute little, while distinctive, resume-specific terms carry more weight.

**Cosine similarity:** measures the angle between the resume's and job description's TF-IDF vectors — a score close to 1 means the two documents emphasize similar content, close to 0 means they don't, regardless of document length.

**Skill matching:** runs separately from the similarity score, using word-boundary-aware keyword matching against a fixed skill dictionary to explicitly list matched and missing skills — giving actionable detail beyond a single number.

## Known Limitations

TF-IDF is purely frequency-based — it has no semantic understanding. Two resumes phrased differently but meaning the same thing (e.g., "led a team" vs. "managed people") can score as dissimilar even though a human reader would treat them the same. Skill matching is exact-token based against a fixed dictionary scoped to tech/IT roles — it won't recognize skills outside that dictionary or industries outside tech. Both are known, understood limitations of the approach, not oversights.

---

## Running Locally

```bash
git clone https://github.com/rumaisemhmd/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Environment variables

Create a `.env` file in the project root (see `.env.example`):

```
SECRET_KEY=your-django-secret-key
DATABASE_URL=postgres://user:password@host:port/dbname
GOOGLE_CLIENT_ID=your-google-oauth-client-id
GOOGLE_CLIENT_SECRET=your-google-oauth-client-secret
```

`GOOGLE_CLIENT_ID`/`GOOGLE_CLIENT_SECRET` come from a Google Cloud OAuth 2.0 Web application client, with `http://127.0.0.1:8000/accounts/google/login/callback/` added as an authorized redirect URI for local development.

### Migrate and run

```bash
python manage.py migrate
python manage.py runserver
```

The app will be available at `http://127.0.0.1:8000/`.

---

## Future Improvements

- Replace/supplement TF-IDF with sentence embeddings (e.g., Sentence-BERT) for meaning-based matching rather than pure word overlap
- Build a labeled evaluation set (human-scored resume/job-description pairs) to formally measure matching accuracy, rather than relying on informal review
- Introduce a vector database for efficient matching against a large set of job descriptions at once, if scaled beyond one-to-one comparisons

---

## Author

Mohammed Rumaise A
GitHub: https://github.com/rumaisemhmd LinkedIn: https://linkedin.com/in/mohammed-rumaise-a-dev
