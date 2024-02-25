# responses.py
import ollama

def get_response(model: str, user_input: str) -> str:
    response = ollama.chat(model=model, messages=[
        {
            'role': 'user',
            'content': user_input,
        },
    ])
    return response['message']['content']