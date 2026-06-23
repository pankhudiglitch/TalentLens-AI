KEYWORDS = [

    "ai",
    "machine learning",
    "ml",
    "llm",
    "retrieval",
    "ranking",
    "python",
    "nlp",
    "cloud",
    "embedding"

]


def score_candidate(candidate, job_text):

    profile = candidate.get(
        "profile",
        {}
    )

    headline = str(
        profile.get(
            "headline",
            ""
        )
    ).lower()

    summary = str(
        profile.get(
            "summary",
            ""
        )
    ).lower()

    combined = headline + " " + summary

    score = 0

    years = profile.get(
        "years_of_experience",
        0
    )

    score += min(
        years * 3,
        30
    )

    for word in KEYWORDS:

        if (
            word in combined
            and
            word in job_text.lower()
        ):

            score += 8

    signals = candidate.get(
        "redrob_signals",
        {}
    )

    score += min(

        signals.get(
            "github_activity_score",
            0
        ),

        10

    )

    if signals.get(
        "open_to_work_flag",
        False
    ):
        score += 5

    return round(
        score,
        1
    )