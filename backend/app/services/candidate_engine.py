from sentence_transformers import SentenceTransformer


model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def candidate_embedding(candidate):

    text = str(candidate)

    embedding = model.encode(
        text
    )

    return embedding.tolist()