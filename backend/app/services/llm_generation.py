import os
import google.generativeai as genai
from typing import Optional, List, Dict, Any, AsyncGenerator

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
                                 chat_history: Optional[List[Dict[str, str]]] = None) -> AsyncGenerator[str, None]:
        """
        Generates a response using the Gemini LLM, incorporating retrieved context and chat history.
        """
        
        # Prepare messages for Gemini API, ensuring correct roles
        messages = []
        if chat_history:
            for msg in chat_history:
                # Gemini roles are 'user' and 'model'. Any other role will cause an error.
                # We map 'assistant' or any other non-user role to 'model'.
                role = "model" if msg.role != "user" else "user"
                messages.append({"role": role, "parts": [msg.content]})
        
        # Add the current prompt (user message + context)
        messages.append({"role": "user", "parts": [prompt]})
        
        try:
            # Start a chat session with the model, excluding the last message which is the current prompt
            chat_session = self.model.start_chat(history=messages[:-1])
            
            # Send the current message (prompt) and stream the response
            response = await chat_session.send_message_async(messages[-1]["parts"], stream=True)
            
            async for chunk in response:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            yield f"Error generating response from Gemini: {e}"
