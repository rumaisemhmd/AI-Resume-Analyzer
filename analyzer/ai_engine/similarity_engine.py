from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity(resume_text, job_description):

    documents = [resume_text, job_description]

    vectorizer = TfidfVectorizer()

    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )

    return round(similarity[0][0] * 100, 2)

def calculate_final_score(tfidf_score, matched_skills, total_required_skills):

    if total_required_skills == 0:
        skill_score = 0
    else:
        skill_score = (matched_skills / total_required_skills) * 100

    final_score = (0.30 * tfidf_score) + (0.70 * skill_score)

    return round(final_score, 2)