from openai import OpenAI

client = OpenAI()

def answer_question(question: str) -> str:
    # This is plain prompting, NOT a RAG pipeline. No retrieval is implemented.
    result = client.chat.completions.create(
        model='gpt-4.1-mini',
        messages=[{'role':'user','content': question}]
    )
    return result.choices[0].message.content
