from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file if present

# Set your OpenAI API key from environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_chat_response(user_input, chat_history):
    # Update the conversation with user input
    chat_history.append({"role": "user", "content": user_input})

    try:
        # Generate response
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=chat_history,
            temperature=0.7,
        )

        # Extract assistant's reply
        reply = response.choices[0].message.content
        
        # Add the assistant's response to chat history
        chat_history.append({"role": "assistant", "content": reply})
        
        return reply
    except Exception as e:
        print(f"Error occurred: {e}")
        return f"An error occurred: {str(e)}"
