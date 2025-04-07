# codeanalyzer/deepseek.py

import requests
import json
from codeanalyzer.config import Config

class DeepSeekClient:
    LANG_MAP = {
        'en': 'English',
        'uz': 'Uzbek',
        'zh': 'Chinese',
        'ru': 'Russian'
    }

    @staticmethod
    def analyze_code(code, lang='en'):
        language_name = DeepSeekClient.LANG_MAP.get(lang, 'English')
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {Config.DEEPSEEK_API_KEY}"
        }

        payload = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "system",
                    "content": f"You are a security expert analyzing code for vulnerabilities and bugs. "
                               f"Identify and explain any issues found. Keep responses concise. Respond in {language_name}."
                },
                {
                    "role": "user",
                    "content": f"Analyze this code for security vulnerabilities and bugs:\n\n{code}"
                }
            ],
            "temperature": 0.2
        }

        response = requests.post(
            Config.DEEPSEEK_API_URL,
            headers=headers,
            json=payload,
            timeout=Config.REQUEST_TIMEOUT
        )
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']

    @staticmethod
    def generate_summary_streaming(findings, lang='en'):
        language_name = DeepSeekClient.LANG_MAP.get(lang, 'English')
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {Config.DEEPSEEK_API_KEY}"
        }

        payload = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "system",
                    "content": f"Summarize security findings into a clear report. Highlight critical issues. Respond in {language_name}."
                },
                {
                    "role": "user",
                    "content": f"Summarize these findings:\n\n{findings}"
                }
            ],
            "temperature": 0.2,
            "stream": True
        }

        response = requests.post(
            Config.DEEPSEEK_API_URL,
            headers=headers,
            json=payload,
            stream=True,
            timeout=Config.REQUEST_TIMEOUT
        )
        response.raise_for_status()

        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                if decoded_line.startswith("data: "):
                    json_data = decoded_line[6:]
                    if json_data.strip() == "[DONE]":
                        break
                    try:
                        data = json.loads(json_data)
                        yield data['choices'][0]['delta'].get('content', '')
                    except json.JSONDecodeError:
                        continue