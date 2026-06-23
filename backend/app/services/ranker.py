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


def shortlist_candidates():

    data = load_candidates()

    ranked = []

    for candidate in data[:1000]:

        profile = candidate.get(
            "profile",
            {}
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
            profile.get(
                "headline"
            ),

            "experience":
            profile.get(
                "years_of_experience"
            ),

            "score":
            score_candidate(
                candidate,
                JOB_TEXT
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