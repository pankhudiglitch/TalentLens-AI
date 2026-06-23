from app.services.load_data import load_candidates
from app.services.scorer import score_candidate
from app.services.export import export_results


JOB_TEXT = """

Senior AI Engineer

Python
Machine Learning
LLM
Retrieval
Ranking
Cloud
Embeddings

"""


def detect_skills(text):

    text = str(text).lower()

    skills = []

    mapping = {

        "AI":
        ["ai"],

        "Machine Learning":
        ["ml", "machine learning"],

        "Python":
        ["python"],

        "Cloud":
        ["cloud"],

        "LLM":
        ["llm"],

        "Retrieval":
        ["retrieval"]

    }

    for label, words in mapping.items():

        if any(
            w in text
            for w in words
        ):

            skills.append(
                label
            )

    return skills[:4]


def explain_candidate(score):

    why = []

    if score >= 68:
        why.append(
            "Strong overall fit"
        )

    if score >= 65:
        why.append(
            "Relevant experience"
        )

    if score >= 60:
        why.append(
            "Good candidate signals"
        )

    return why[:3]


def shortlist_candidates():

    data = load_candidates()

    ranked = []

    for candidate in data[:1000]:

        profile = candidate.get(
            "profile",
            {}
        )

        headline = profile.get(
            "headline",
            ""
        )

        score = score_candidate(
            candidate,
            JOB_TEXT
        )

        ranked.append({

            "candidate_id":
            candidate.get(
                "candidate_id"
            ),

            "name":
            profile.get(
                "anonymized_name"
            ),

            "headline":
            headline,

            "experience":
            profile.get(
                "years_of_experience"
            ),

            "score":
            score,

            "skills":
            detect_skills(
                headline
            ),

            "why":
            explain_candidate(
                score
            )

        })

    ranked.sort(
        key=lambda x:
        x["score"],
        reverse=True
    )

    top = ranked[:10]

    export_results(
        top
    )

    return {

        "job_loaded": True,

        "processed": 1000,

        "top_candidates": top

    }