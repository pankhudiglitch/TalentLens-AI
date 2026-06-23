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


def discover_skills(text):

    skills = []

    mapping = {

        "backend":
        ["api", "backend", "server"],

        "machine_learning":
        ["ml", "machine learning"],

        "llm":
        ["llm", "language model"],

        "cloud":
        ["cloud", "aws"],

        "retrieval":
        ["retrieval", "ranking"],

        "analytics":
        ["data", "analytics"]

    }

    for skill, words in mapping.items():

        if any(
            w in text
            for w in words
        ):

            skills.append(
                skill
            )

    return skills


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

    explain = []

    years = profile.get(
        "years_of_experience",
        0
    )

    exp_score = min(
        years * 3,
        30
    )

    score += exp_score

    if exp_score > 15:
        explain.append(
            "Strong experience fit"
        )

    skill_score = 0

    for word in KEYWORDS:

        if (
            word in combined
            and
            word in job_text.lower()
        ):

            skill_score += 6

    score += skill_score

    if skill_score:
        explain.append(
            "Relevant AI skills"
        )

    signals = candidate.get(
        "redrob_signals",
        {}
    )

    github = min(
        signals.get(
            "github_activity_score",
            0
        ),
        10
    )

    score += github

    if github > 3:
        explain.append(
            "Strong activity signals"
        )

    growth = 0

    if years <= 8:
        growth = 10

    score += growth

    if growth:
        explain.append(
            "High growth potential"
        )

    hidden = discover_skills(
        combined
    )

    return {

        "score":
        round(
            score,
            1
        ),

        "hidden_skills":
        hidden,

        "why":
        explain[:3]

    }