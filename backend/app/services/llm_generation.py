import os
import google.generativeai as genai
from typing import Optional, List, Dict, Any, AsyncGenerator
from app.models.api_models import ChatMessage # Import ChatMessage

class LLMGenerationService:
    def __init__(self):
        self.api_key = os.getenv("LLM_API_KEY")
        self.model_name = os.getenv("LLM_MODEL_NAME")
        
        if not self.api_key:
            raise ValueError("LLM_API_KEY environment variable not set for Gemini.")
        if not self.model_name:
            raise ValueError("LLM_MODEL_NAME environment variable not set for Gemini.")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)

    async def generate_response(self, 
                                 prompt: str, 
                                 retrieved_context: List[Dict[str, Any]],
                                 chat_history: Optional[List[ChatMessage]] = None) -> AsyncGenerator[str, None]: # Use ChatMessage type hint
        """
        Generates a response using the Gemini LLM, incorporating retrieved context and chat history.
        """
        
        messages = []
        if chat_history:
            for msg in chat_history:
                role = "model" if msg.role != "user" else "user" # Access attributes using .role
                messages.append({"role": role, "parts": [msg.content]}) # Access attributes using .content
        
        messages.append({"role": "user", "parts": [prompt]})
        
        try:
            chat_session = self.model.start_chat(history=messages[:-1])
            response = await chat_session.send_message_async(messages[-1]["parts"][0], stream=True)
            
            async for chunk in response:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            yield f"Error generating response from Gemini: {e}"