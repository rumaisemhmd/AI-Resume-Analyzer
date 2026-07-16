def generate_recommendation(score, missing_skills):

    if score >= 80:
        return "Excellent match! Your resume closely matches the job description."

    elif score >= 60:
        return (
            "Good match. Improve your resume by adding: "
            + missing_skills
        )

    elif score >= 40:
        return (
            "Average match. Consider improving your projects, summary, and adding these skills: "
            + missing_skills
        )

    else:
        return (
            "Low match. Tailor your resume to the job description and learn these skills: "
            + missing_skills
        )