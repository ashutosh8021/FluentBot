from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file if present

# Set your OpenAI API key from environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_chat_response(user_input, chat_history):
    # Update the conversation
    chat_history.append({"role": "user", "content": user_input})

    # Generate response
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=chat_history,
        temperature=0.7,
    )

    # Extract assistant's reply
    reply = response.choices[0].message.content
    return reply
