import csv
import os


def export_results(results):

    os.makedirs(
        "outputs",
        exist_ok=True
    )

    path = "outputs/ranked_candidates.csv"

    with open(
        path,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.DictWriter(

            f,

            fieldnames=[

                "candidate_id",
                "name",
                "headline",
                "experience",
                "score"

            ]

        )

        writer.writeheader()

        writer.writerows(
            results
        )

    return path