import re

SKILLS = [

    "python", "java", "c", "c++", "c#", "javascript", "typescript", "php", "go", "rust",


    "html", "css", "bootstrap", "tailwind", "react", "angular", "vue",


    "django", "flask", "fastapi", "node.js", "express", "spring boot",

    "mysql", "postgresql", "mongodb", "sqlite", "oracle", "redis",


    "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "terraform",


    "rest api", "graphql", "git", "github", "postman", "swagger",


    "numpy", "pandas", "scikit-learn", "tensorflow", "keras", "pytorch",
    "opencv", "nltk", "spacy", "machine learning", "deep learning",
    "artificial intelligence", "computer vision", "nlp",


    "power bi", "tableau", "excel", "sql",


    "pytest", "selenium", "unittest",


    "ci/cd", "linux", "nginx", "gunicorn", "render", "heroku", "vercel",


    "rag", "llm", "embeddings", "vector database", "pgvector",
    "prompt engineering", "agentic ai", "hugging face", "langchain",


    "oauth", "oauth2", "jwt", "authentication",


    "jest", "cypress",


    "agile", "scrum", "ci", "api design", "microservices", "websockets", "celery"
]


def _skill_pattern(skill):
    # A skill only counts as present if it's not glued to another
    # alphanumeric character on either side -- e.g. "go" inside "django"
    # or "sql" inside "mysql" must NOT count as a match.
    return re.compile(r"(?<![a-z0-9])" + re.escape(skill.lower()) + r"(?![a-z0-9])")


def extract_skills(text):

    text = text.lower()

    claimed_spans = []
    found = set()

    # Longest skill names first, so e.g. "c++"/"c#" claim their text
    # before plain "c" gets a chance to falsely match the same spot
    # (a boundary check alone can't tell "c" apart from "c++"/"c#",
    # since "+" and "#" aren't alphanumeric either).
    for skill in sorted(SKILLS, key=len, reverse=True):

        pattern = _skill_pattern(skill)

        for match in pattern.finditer(text):

            start, end = match.span()

            overlaps = any(start < s_end and end > s_start for s_start, s_end in claimed_spans)

            if overlaps:
                continue

            claimed_spans.append((start, end))
            found.add(skill)
            break

    return [skill for skill in SKILLS if skill in found]


def missing_skills(resume_skills, job_skills):

    missing = []

    for skill in job_skills:

        if skill not in resume_skills:
            missing.append(skill)

    return missing


def matched_skills(resume_skills, job_skills):

    matched = []

    for skill in resume_skills:

        if skill in job_skills:
            matched.append(skill)

    return matched
