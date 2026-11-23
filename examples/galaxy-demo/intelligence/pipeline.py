from intelligence.embed import fake_embedding

def answer(question: str):
    return {'note': 'No trained model or RAG is implemented here.', 'vector': fake_embedding(question)}
