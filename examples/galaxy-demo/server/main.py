from fastapi import FastAPI
from intelligence.pipeline import answer
from storage.db import recent_count
app = FastAPI()

@app.get('/status')
def status():
    return {'count': recent_count(), 'demo': answer('hello')}
