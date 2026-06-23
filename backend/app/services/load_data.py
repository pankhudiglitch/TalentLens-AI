import json
import os


def load_candidates():

    path = os.path.join(
        "app",
        "data",
        "[PUB] India_runs_data_and_ai_challenge",
        "India_runs_data_and_ai_challenge",
        "candidates.jsonl"
    )

    print("USING FILE:", path)

    candidates = []

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        for line in f:

            if line.strip():

                candidates.append(
                    json.loads(line)
                )

    return candidates