from fastapi import FastAPI
from rag import answer_question
app = FastAPI()

@app.get('/health')
def health():
    return {'status':'ok'}

@app.post('/ask')
def ask(question: str):
    return {'answer': answer_question(question)}
