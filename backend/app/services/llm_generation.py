import os
import google.generativeai as genai
from typing import Optional, List, Dict, Any, AsyncGenerator

class LLMGenerationService:
    def __init__(self):
        self.api_key = os.getenv("LLM_API_KEY")
        self.model_name = os.getenv("LLM_MODEL_NAME", "gemini-2.5")
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
        else:
            print("WARNING: LLM_API_KEY not set. Gemini LLM will be disabled.")
            self.model = None

    async def generate_response(
        self,
        prompt: str,
        retrieved_context: List[Dict[str, Any]],
        chat_history: Optional[List[Dict[str, str]]] = None
    ) -> AsyncGenerator[str, None]:

        if not self.model:
            # Yield immediately if model not configured
            yield "Error: LLM model not configured. Please set LLM_API_KEY.\n"
            return

        messages = []
        if chat_history:
            for msg in chat_history:
                role = "model" if msg.get("role") != "user" else "user"
                messages.append({"role": role, "parts": [msg.get("content", "")]})
        messages.append({"role": "user", "parts": [prompt]})

        try:
            chat_session = self.model.start_chat(history=messages[:-1])
            response = await chat_session.send_message_async(messages[-1]["parts"], stream=True)

            async for chunk in response:
                if chunk.text:
                    yield chunk.text

        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            # Yield an error immediately so frontend stops waiting
            yield f"Error generating response from Gemini: {e}\n"
