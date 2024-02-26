# responses.py
import ollama

def get_response(model: str, user_input: str) -> str:
    response = ollama.chat(
        model=model, 
        messages=[
            {
                'role': 'user',
                'content': user_input,
            }
        ],
        stream=True
    )
    return response



def test_get_response():
    while True:
        user_input = input("YOU: ")
        stream = get_response(model="gemma:2b", user_input=user_input)
        for chunk in stream:
            print(chunk['message']['content'], end='', flush=True)
        print()
    
if __name__ == '__main__':
    test_get_response()