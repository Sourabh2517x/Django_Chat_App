import google.generativeai as genai
from django.conf import settings
from google.api_core.exceptions import ResourceExhausted, ServiceUnavailable
from .utils import parse_response

genai.configure(api_key=settings.GEMINI_API_KEY)


class GeminiService:
    def __init__(self, model_name="gemini-2.5-flash"):
        self.model = genai.GenerativeModel(model_name)

    def format_messages(self, conversation):
        return [
            {
                "role": "user" if msg.sender == "user" else "model",
                "parts": [msg.content],
            }
            for msg in conversation.messages.order_by("created")
        ]

    def generate_response(self, conversation, user_input):
        system_prompt = """
        You are a Django expert assistant.

        Rules:
        - Only answer questions related to Django.
        - If unrelated, politely refuse in 1–2 lines.
        - Use clean formatting:
        - Use bullet points when needed
        - Use short paragraphs
        - Use code blocks for code
        - Keep answers clear and practical.
        """

        messages = self.format_messages(conversation)
        messages.insert(0, {"role": "user", "parts": [system_prompt]})
        messages.append({"role": "user", "parts": [user_input]})

        try:
            response = self.model.generate_content(messages)
        except ResourceExhausted:
            raise GeminiServiceError("Rate limit exceeded", 429)
        except ServiceUnavailable:
            raise GeminiServiceError("Model busy, try again later", 503)
        except Exception:
            raise GeminiServiceError("Unexpected error occurred", 500)

        clean_html, tokens_used = parse_response(response)

        return clean_html, tokens_used


class GeminiServiceError(Exception):
    def __init__(self, message, status_code=500):
        self.message = message
        self.status_code = status_code
        super().__init__(message)
