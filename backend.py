import os
import streamlit as st

# Check if OpenAI is installed, if not use a fallback approach
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

def get_chat_response(user_input, chat_history):
    """
    Process user input and return a response.
    Uses OpenAI if available, otherwise falls back to a simple rule-based response.
    """
    # If OpenAI is available and configured
    if OPENAI_AVAILABLE:
        try:
            # Try to get API key from environment or Streamlit secrets
            api_key = os.environ.get("OPENAI_API_KEY") 
            
            # If using Streamlit secrets (recommended for security)
            if not api_key and hasattr(st, "secrets") and "openai_api_key" in st.secrets:
                api_key = st.secrets["openai_api_key"]
                
            if api_key:
                client = OpenAI(api_key=api_key)
                
                # Format the conversation history for OpenAI
                messages = []
                for msg in chat_history:
                    messages.append({"role": msg["role"], "content": msg["content"]})
                
                # Add the latest user message
                messages.append({"role": "user", "content": user_input})
                
                # Call OpenAI API
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    max_tokens=500,
                    temperature=0.7
                )
                
                return response.choices[0].message.content
            else:
                return "OpenAI API key not found. Please set the OPENAI_API_KEY environment variable or add it to your Streamlit secrets."
        except Exception as e:
            return f"An error occurred with the OpenAI API: {str(e)}"
    
    # Fallback: Simple rule-based responses
    else:
        # Simple rule-based response system
        user_input_lower = user_input.lower()
        
        if "hello" in user_input_lower or "hi" in user_input_lower:
            return "Hello! How can I help with your studies today?"
        
        elif "study" in user_input_lower or "learn" in user_input_lower:
            return "Effective study techniques include active recall, spaced repetition, and the Pomodoro technique. Which subject are you studying?"
        
        elif "math" in user_input_lower or "mathematics" in user_input_lower:
            return "Mathematics requires practice. Try solving problems regularly and understand the concepts rather than memorizing formulas."
        
        elif "science" in user_input_lower:
            return "For science subjects, try to connect concepts with real-world examples and visualize processes when possible."
        
        elif "history" in user_input_lower:
            return "When studying history, create timelines and connect events to understand cause and effect relationships better."
        
        elif "language" in user_input_lower or "english" in user_input_lower:
            return "Language learning is enhanced by regular practice. Try reading books, watching shows, or finding conversation partners."
        
        elif "tired" in user_input_lower or "break" in user_input_lower:
            return "Taking breaks is important! Consider the Pomodoro technique: 25 minutes of focused study followed by a 5-minute break."
        
        elif "thank" in user_input_lower:
            return "You're welcome! Feel free to ask if you have more questions."
        
        else:
            return "That's an interesting question about your studies. Could you provide more details so I can give you a better answer?"
