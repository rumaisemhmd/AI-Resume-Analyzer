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

    
    "pytest", "selenium", "unittest"
]
def extract_skills(text):

    text = text.lower()

    found = []

    for skill in SKILLS:

        if skill.lower() in text:
            found.append(skill)

    return found
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