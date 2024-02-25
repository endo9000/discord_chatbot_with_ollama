# ollama.py

import json
import requests

class ChatOllama:
    def __init__(self, model, temperature, base_url="http://localhost:11434/api/chat", ai_name=None):
        self.model = model
        self.temperature = temperature
        self.base_url = base_url
        self.ai_name = ai_name

    def chat(self, message, output=False, stream=True):
        data = {"model": self.model, "messages": message, "stream": stream}
        if stream:
            response = self._make_streaming_request(data)
            self._stream_output(response, output)
            return response
        else:
            response = self._make_standard_request(data)
            self._print_output(response, output)
            return response

    def _make_streaming_request(self, data):
        return requests.post(self.base_url, json=data, stream=True)

    def _make_standard_request(self, data):
        return requests.post(self.base_url, json=data, stream=False)

    def _stream_output(self, response, output):
        first_chunk = True
        complete_content = []
        for chunk in response.iter_content(chunk_size=None):
            if chunk:
                content = self._extract_content_from_chunk(chunk)
                if output:
                    self._print_chunk_content(content, first_chunk)
                    first_chunk = False
                complete_content.append(content)
        print()

    def _extract_content_from_chunk(self, chunk):
        return json.loads(chunk.decode('utf-8')).get("message", {}).get("content", "")

    def _print_chunk_content(self, content, first_chunk):
        if first_chunk:
            print(f"{self.ai_name}: {content}", end='', flush=True)
        else:
            print(content, end='', flush=True)

    def _print_output(self, response, output):
        content = response.json()["message"]["content"]
        if output:
            print(f"{self.ai_name}: {content}")
        return content


class ChatMemory:
    def __init__(self, k=None):
        self.k = k
        self.messages = []

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})
        if self.k is not None:
            self.messages = self.messages[-self.k:]


class ChatManager:
    def __init__(self, llm, memory=None, tools=None):
        self.llm = llm
        self.memory = memory
        self.tools = tools

    def start(self, prompt, output=False, stream=True):
        if self.memory:
            self.memory.add_message("user", prompt)
            response = self.llm.chat(message=self.memory.messages, output=output, stream=stream)
            self.memory.add_message("assistant", response)
        else:
            chat_input = [{"role": "user", "content": prompt}]
            response = self.llm.chat(message=chat_input, output=output, stream=stream)
        return response
