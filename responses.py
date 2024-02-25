# responses.py
import ollama

system_prompt = """"""

model = "gemma:2b_c"

print(ollama.generate(model=model, keep_alive="5s", options={"temperature": 0, "num_ctx": 4096}, prompt=system_prompt, format="json"))