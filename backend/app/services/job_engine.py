from sentence_transformers import SentenceTransformer
from docx import Document
import json
import os
import numpy as np


model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def similarity(a, b):

    a = np.array(a)

    b = np.array(b)

    return float(

        np.dot(a, b)

        /

        (

            np.linalg.norm(a)

            *

            np.linalg.norm(b)

        )

    )


def load_job_description():

    path = os.path.join(

        "app",

        "data",

        "[PUB] India_runs_data_and_ai_challenge",

        "India_runs_data_and_ai_challenge",

        "job_description.docx"

    )

    doc = Document(path)

    text = []

    for p in doc.paragraphs:

        if p.text:

            text.append(

                p.text

            )

    return "\n".join(

        text

    )


def get_job_embedding():

    text = load_job_description()

    return model.encode(text)


def shortlist_candidates():

    path = os.path.join(

        "app",

        "data",

        "[PUB] India_runs_data_and_ai_challenge",

        "India_runs_data_and_ai_challenge",

        "candidates.jsonl"

    )

    print("USING FILE:", path)

    job_vector = get_job_embedding()

    candidates = []

    texts = []

    processed = 0

    with open(

        path,

        "r",

        encoding="utf-8"

    ) as f:

        for line in f:

            if processed >= 1000:

                break

            row = json.loads(line)

            profile = row.get(

                "profile",

                {}

            )

            skills = row.get(

                "skills",

                []

            )

            history = row.get(

                "career_history",

                []

            )

            text = " ".join([

                profile.get(

                    "headline",

                    ""

                ),

                profile.get(

                    "summary",

                    ""

                ),

                " ".join([

                    s.get(

                        "name",

                        ""

                    )

                    for s in skills

                ]),

                " ".join([

                    h.get(

                        "title",

                        ""

                    )

                    for h in history[:2]

                ])

            ])

            if not text.strip():

                continue

            candidates.append(row)

            texts.append(text)

            processed += 1

    print("Encoding candidates...")

    embeddings = model.encode(

        texts,

        batch_size=128,

        show_progress_bar=False

    )

    ranked = []

    for row, emb in zip(

        candidates,

        embeddings

    ):

        profile = row.get(

            "profile",

            {}

        )

        score = similarity(

            job_vector,

            emb

        ) * 100

        years = float(

            profile.get(

                "years_of_experience",

                0

            )

        )

        if 5 <= years <= 9:

            score += 6

        title = str(

            profile.get(

                "current_title",

                ""

            )

        ).lower()

        if (

            "ml" in title

            or

            "ai" in title

            or

            "data scientist" in title

            or

            "machine learning" in title

        ):

            score += 10

        ranked.append({

            "candidate_id":

            row.get(

                "candidate_id"

            ),

            "name":

            profile.get(

                "anonymized_name",

                "Unknown"

            ),

            "headline":

            profile.get(

                "headline",

                ""

            ),

            "experience":

            years,

            "score":

            round(

                score,

                1

            )

        })

    ranked.sort(

        key=lambda x:

        x["score"],

        reverse=True

    )

    return {

        "job_loaded": True,

        "processed": processed,

        "top_candidates":

        ranked[:10]

    }