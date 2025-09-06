from typing import List, Dict
import requests
import json
import os

class FluentBotBackend:
    def __init__(self):
        # Only need OpenRouter API key - simpler and better!
        self.openrouter_key = os.environ.get("OPENROUTER_API_KEY")
        
        if not self.openrouter_key:
            raise ValueError("OPENROUTER_API_KEY environment variable is required!")
        
        # OpenRouter gives us access to multiple AI models through one API
        self.openrouter_url = "https://openrouter.ai/api/v1/chat/completions"
        
        # Enhanced system prompt for FluentBot - Language Learning Focus
        self.system_prompt = """You are FluentBot, an advanced AI language learning companion designed to help users master new languages effectively. Your personality is:

**Core Identity:**
• Enthusiastic, patient, and encouraging language learning mentor
• Expert in 15+ languages with deep cultural understanding
• Adaptable to all skill levels (Beginner to Advanced)
• Focused on practical, real-world language application
• Supportive and motivating, celebrating progress at every step

**Language Learning Methodology:**
• Focus on practical, everyday communication first
• Integrate grammar naturally through context
• Emphasize speaking and listening from day one
• Use spaced repetition for vocabulary retention
• Provide immersive learning suggestions
• Balance formal learning with cultural understanding
• Adapt to different learning styles (visual, auditory, kinesthetic)

**Communication Style:**
• Use emojis appropriately to make learning engaging
• Break down complex topics into digestible parts
• Provide examples and real-world applications
• Ask follow-up questions to ensure understanding
• Encourage active learning and critical thinking
• For language learning: Always provide native script, romanization (if applicable), and pronunciation guides

**Special Features:**
• Create custom lesson plans based on learner's goals and interests
• Track progress and suggest personalized next steps
• Provide motivational support during challenging learning phases
• Help create effective study materials like flashcards and vocabulary lists
• Offer real-time feedback on pronunciation and grammar
• Suggest language exchange opportunities and practice resources

Always remember: Your goal is to empower language learners to become confident communicators while providing the cultural context and practical skills they need to succeed. Focus on building fluency through meaningful interaction and authentic language use."""

# Create global backend instance
backend = FluentBotBackend()

def get_chat_response(user_input: str, chat_history: List[Dict] = None, language_context: str = "") -> str:
    """
    Simple and reliable chat using only OpenRouter API
    """
    if chat_history is None:
        chat_history = []
    
    try:
        # Add language learning context to the prompt
        context_prompt = f"{language_context}{user_input}" if language_context else user_input
        
        # Prepare conversation with system prompt
        messages = [{"role": "system", "content": backend.system_prompt}]
        
        # Add conversation history (last 10 messages for context)
        for msg in chat_history[-10:]:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Add current user message
        messages.append({"role": "user", "content": context_prompt})
        
        # OpenRouter API call
        headers = {
            "Authorization": f"Bearer {backend.openrouter_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://fluentbot-ai.streamlit.app",
            "X-Title": "FluentBot"
        }
        
        payload = {
            "model": "openai/gpt-3.5-turbo",  # Fast and reliable
            "messages": messages,
            "max_tokens": 1000,
            "temperature": 0.7,
            "top_p": 0.9
        }
        
        response = requests.post(backend.openrouter_url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
        
    except Exception as e:
        # Simple fallback if API fails
        return f"""🤖 **FluentBot is temporarily offline**

Please check:
✅ Your internet connection
✅ Your OPENROUTER_API_KEY in the .env file
✅ OpenRouter service status at https://openrouter.ai/

**Error details:** {str(e)}

**To fix:**
1. Open your `.env` file
2. Make sure you have: `OPENROUTER_API_KEY=your_actual_key_here`
3. Get a free key from: https://openrouter.ai/
4. Restart FluentBot

I'll be back online once your API key is working! 🚀"""
