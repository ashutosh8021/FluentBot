# Load environment variables FIRST - before any other imports
import os

# Try to load dotenv with error handling
try:
    from dotenv import load_dotenv
    load_dotenv()  # Load .env file if available
except ImportError:
    # If dotenv is not available (like in some cloud environments), that's okay
    # Environment variables can still be set directly
    pass

import streamlit as st

st.set_page_config(
    page_title="FluentBot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "FluentBot - Your intelligent language learning companion powered by advanced AI"
    }
)

import time
import random
from typing import List, Dict
from datetime import datetime

# Check for required API key - check both env vars and Streamlit secrets
api_key = os.environ.get("OPENROUTER_API_KEY")

# If not in environment variables, try Streamlit secrets
if not api_key:
    try:
        api_key = st.secrets["OPENROUTER_API_KEY"]
    except:
        pass

if not api_key:
    st.error("⚠️ OPENROUTER_API_KEY not found!")
    
    st.markdown("""
    ### 🔑 How to add your API key:
    
    **For Local Development:**
    1. Create a `.env` file in your project root
    2. Add: `OPENROUTER_API_KEY=your_key_here`
    3. Restart the app
    
    **For Streamlit Cloud:**
    1. Go to your app settings
    2. Add `OPENROUTER_API_KEY` to secrets
    3. Redeploy the app
    
    **Get your free API key:** https://openrouter.ai/
    """)
    st.stop()

# Set the API key in environment for backend to use
os.environ["OPENROUTER_API_KEY"] = api_key

# Try to import backend
try:
    from backend import get_chat_response
    backend_available = True
except Exception as e:
    backend_available = False
    st.error(f"Backend not available: {str(e)}")

# Enhanced CSS with dark ChatGPT-inspired theme
st.markdown("""
<style>
/* Dark theme variables */
:root {
    --bg-color: #212121;
    --secondary-bg: #2f2f2f;
    --text-color: #ffffff;
    --accent-color: #10a37f;
    --border-color: #404040;
    --hover-color: #404040;
}

/* Main app background */
.stApp {
    background-color: var(--bg-color);
    color: var(--text-color);
}

/* Sidebar styling */
.css-1d391kg {
    background-color: var(--secondary-bg);
}

/* Main content area */
.main .block-container {
    padding-top: 2rem;
    background-color: var(--bg-color);
}

/* Headers */
.main-header {
    text-align: center;
    padding: 2rem 0;
    border-bottom: 1px solid var(--border-color);
    margin-bottom: 2rem;
}

.main-header h1 {
    color: var(--accent-color);
    font-size: 3rem;
    margin-bottom: 0.5rem;
    font-weight: 700;
}

.main-header p {
    color: var(--text-color);
    font-size: 1.2rem;
    opacity: 0.8;
}

/* Chat interface */
.chat-container {
    max-height: 600px;
    overflow-y: auto;
    padding: 1rem;
    background: var(--secondary-bg);
    border-radius: 12px;
    border: 1px solid var(--border-color);
    margin-bottom: 1rem;
}

/* Message styling */
.user-message {
    background: var(--accent-color);
    color: white;
    padding: 12px 16px;
    border-radius: 18px 18px 4px 18px;
    margin: 8px 0;
    margin-left: 20%;
    font-size: 0.95rem;
}

.assistant-message {
    background: var(--secondary-bg);
    color: var(--text-color);
    padding: 12px 16px;
    border-radius: 18px 18px 18px 4px;
    margin: 8px 0;
    margin-right: 20%;
    border: 1px solid var(--border-color);
    font-size: 0.95rem;
}

/* Button styling */
.stButton > button {
    background: var(--accent-color);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    font-weight: 600;
    transition: all 0.2s;
}

.stButton > button:hover {
    background: #0d8f6e;
    transform: translateY(-1px);
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Set up initial session state variables
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.chat_history = []
    st.session_state.use_ai = True

# Main app layout
st.markdown("""
    <div class="main-header">
        <h1>🤖 FluentBot</h1>
        <p>Your intelligent language learning companion</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar with dark theme
with st.sidebar:
    # Clean header
    st.markdown("### 🤖 FluentBot")
    
    # Language Learning Mode
    st.markdown("### 🌐 Language Learning Mode")
    
    st.info("💡 Select a language and start your learning journey with AI-powered assistance!")
    
    st.markdown("---")
    
    # Quick Language Actions
    st.markdown("### ⚡ Quick Start")
    
    if st.button("🎯 Start Learning", use_container_width=True):
        st.session_state.show_learning_guide = True
    
    if st.button("📈 My Progress", use_container_width=True):
        st.session_state.show_progress = True
    
    st.markdown("---")

    # 🌍 LANGUAGE LEARNING FEATURES
    st.markdown("### 🌍 Choose Your Language")
    
    # Language selection with flags and names
    languages = [
        "🇫🇷 French", "🇯🇵 Japanese", "🇩🇪 German", "🇪🇸 Spanish", "🇮🇹 Italian",
        "🇰🇷 Korean", "🇨🇳 Chinese (Mandarin)", "🇷🇺 Russian", "🇵🇹 Portuguese",
        "🇳🇱 Dutch", "🇸🇦 Arabic", "🇮🇳 Hindi", "🇸🇪 Swedish", "🇳🇴 Norwegian",
        "🇫🇮 Finnish", "🇵🇱 Polish", "🇹🇷 Turkish", "🇬🇷 Greek", "🇮🇱 Hebrew",
        "🇻🇳 Vietnamese", "🇹🇭 Thai"
    ]
    
    selected_language = st.selectbox(
        "Select Language:",
        languages,
        index=0,
        key="language_selection"
    )
    
    # Store selected language
    st.session_state.current_language = selected_language
    
    # Level selection
    levels = ["🌱 Beginner", "📚 Elementary", "🎯 Intermediate", "🚀 Advanced"]
    selected_level = st.selectbox(
        "Your Level:",
        levels,
        index=0,
        key="level_selection"
    )
    
    # Store selected level
    st.session_state.current_level = selected_level
    
    st.markdown("---")
    
    # Feature buttons
    st.markdown("### 🎯 Learning Features")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📅 30-Day Roadmap", use_container_width=True, key="sidebar_roadmap"):
            st.session_state.show_roadmap = True
        
        if st.button("📝 Daily Practice", use_container_width=True, key="sidebar_practice"):
            st.session_state.show_daily_practice = True
    
    with col2:
        if st.button("🧠 Vocabulary Quiz", use_container_width=True, key="sidebar_vocab"):
            st.session_state.show_vocab_quiz = True
        
        if st.button("📖 Grammar Lesson", use_container_width=True, key="sidebar_grammar"):
            st.session_state.show_grammar = True

# Handle Progress display
if st.session_state.get("show_progress"):
    current_lang = st.session_state.get("current_language", "None selected")
    current_level = st.session_state.get("current_level", "None selected")
    
    # Calculate some basic stats
    total_messages = len(st.session_state.chat_history)
    user_messages = len([msg for msg in st.session_state.chat_history if msg["role"] == "user"])
    
    st.info(f"""
    **📊 Your FluentBot Progress Dashboard**
    
    **🌍 Current Learning:**
    • Language: {current_lang}
    • Level: {current_level}
    • Learning Session: Active
    
    **💬 Chat Activity:**
    • Total Messages: {total_messages}
    • Your Questions: {user_messages}
    • AI Responses: {total_messages - user_messages}
    
    **🎯 Today's Goals:**
    • ✅ Selected a language to learn
    • ⏳ Complete 1 vocabulary quiz
    • ⏳ Try daily practice
    • ⏳ Have 5 conversations with FluentBot
    
    **🏆 Achievements:**
    • 🤖 Met FluentBot (Welcome!)
    • 🌍 Chose your learning language
    • 💪 Ready to start your journey!
    
    **📈 Keep Going:** Practice daily for the best results!
    """)
    
    # Progress action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧠 Take Quiz", use_container_width=True, key="progress_quiz"):
            st.session_state.show_vocab_quiz = True
    with col2:
        if st.button("📝 Practice Now", use_container_width=True, key="progress_practice"):
            st.session_state.show_daily_practice = True
    st.session_state.show_progress = False

# Handle Learning Guide display
if st.session_state.get("show_learning_guide"):
    current_lang = st.session_state.get("current_language", "🇫🇷 French")
    current_level = st.session_state.get("current_level", "🌱 Beginner")
    
    st.success(f"""
    **🎯 Welcome to FluentBot Learning! - {current_lang} ({current_level})**
    
    **🚀 Quick Start Options:**
    
    **1. 📅 30-Day Roadmap** - Get your personalized learning path
    **2. 🧠 Vocabulary Quiz** - Test your current knowledge  
    **3. 📝 Daily Practice** - Start with today's challenge
    **4. 📖 Grammar Lesson** - Learn new concepts
    **5. 💬 AI Chat** - Practice conversation with FluentBot
    
    **💡 Recommended for {current_level.split()[1]}s:**
    • Start with Vocabulary Quiz to assess your level
    • Check out the 30-Day Roadmap for structured learning
    • Use Daily Practice for consistent improvement
    • Chat with FluentBot for personalized help
    
    **🎯 Today's Focus:** Master 5 new words and practice one conversation
    """)
    
    # Quick action buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📅 View Roadmap", use_container_width=True, key="guide_roadmap"):
            st.session_state.show_roadmap = True
            st.session_state.show_learning_guide = False
    with col2:
        if st.button("🧠 Start Quiz", use_container_width=True, key="guide_quiz"):
            st.session_state.show_vocab_quiz = True
            st.session_state.show_learning_guide = False
    with col3:
        if st.button("📝 Daily Practice", use_container_width=True, key="guide_practice"):
            st.session_state.show_daily_practice = True
            st.session_state.show_learning_guide = False
    
    st.session_state.show_learning_guide = False

# 🌍 LANGUAGE LEARNING FEATURE HANDLERS
if st.session_state.get("show_roadmap"):
    language = st.session_state.get("current_language", "🇫🇷 French")
    level = st.session_state.get("current_level", "🌱 Beginner")
    
    st.success(f"""
    **📅 30-Day {language} Roadmap - {level}**
    
    **Week 1: Foundation**
    • Days 1-3: Basic greetings and introductions
    • Days 4-5: Numbers 1-100 and time
    • Days 6-7: Family members and personal info
    
    **Week 2: Daily Life**
    • Days 8-10: Food and drinks vocabulary
    • Days 11-12: Present tense verbs
    • Days 13-14: Shopping and prices
    
    **Week 3: Communication**
    • Days 15-17: Directions and locations
    • Days 18-19: Past tense introduction
    • Days 20-21: Describing people and things
    
    **Week 4: Mastery**
    • Days 22-24: Future tense and plans
    • Days 25-27: Cultural topics and traditions
    • Days 28-30: Review and conversation practice
    
    🎯 **Daily Goal**: 30 minutes of practice
    📚 **Resources**: FluentBot AI assistance, vocabulary quizzes, daily practice
    """)
    st.session_state.show_roadmap = False

if st.session_state.get("show_vocab_quiz"):
    language = st.session_state.get("current_language", "🇫🇷 French")
    level = st.session_state.get("current_level", "🌱 Beginner")
    
    # Vocabulary sets based on language and level
    vocab_sets = {
        "🇫🇷 French": {
            "🌱 Beginner": [
                {"word": "Bonjour", "translation": "Hello/Good morning", "pronunciation": "bon-ZHOOR"},
                {"word": "Merci", "translation": "Thank you", "pronunciation": "mer-SEE"},
                {"word": "Au revoir", "translation": "Goodbye", "pronunciation": "oh ruh-VWAHR"},
                {"word": "S'il vous plaît", "translation": "Please", "pronunciation": "see voo PLEH"},
                {"word": "Excusez-moi", "translation": "Excuse me", "pronunciation": "ex-kew-ZAY mwah"},
                {"word": "Je m'appelle", "translation": "My name is", "pronunciation": "zhuh mah-PELL"},
                {"word": "Comment allez-vous?", "translation": "How are you?", "pronunciation": "koh-mahn tah-lay VOO"},
                {"word": "Oui", "translation": "Yes", "pronunciation": "WEE"},
                {"word": "Non", "translation": "No", "pronunciation": "nohn"},
                {"word": "Pardon", "translation": "Sorry/Pardon", "pronunciation": "par-DOHN"}
            ]
        },
        "🇪🇸 Spanish": {
            "🌱 Beginner": [
                {"word": "Hola", "translation": "Hello", "pronunciation": "OH-lah"},
                {"word": "Gracias", "translation": "Thank you", "pronunciation": "GRAH-see-ahs"},
                {"word": "Adiós", "translation": "Goodbye", "pronunciation": "ah-DYOHS"},
                {"word": "Por favor", "translation": "Please", "pronunciation": "por fah-VOR"},
                {"word": "Perdón", "translation": "Excuse me/Sorry", "pronunciation": "per-DOHN"}
            ]
        }
    }
    
    # Get vocabulary for current language/level
    current_vocab = vocab_sets.get(language, {}).get(level, vocab_sets["🇫🇷 French"]["🌱 Beginner"])
    
    # Select a random word if not already selected
    if "current_vocab_word" not in st.session_state:
        st.session_state.current_vocab_word = random.choice(current_vocab)
    
    current_word = st.session_state.current_vocab_word
    
    st.markdown(f"""
    **🧠 Vocabulary Quiz - {language} ({level})**
    
    **Word:** `{current_word['word']}`
    
    **Pronunciation:** *{current_word['pronunciation']}*
    
    What does this word mean in English?
    """)
    
    # Interactive Answer Section
    user_answer = st.text_input(
        "Your answer:",
        placeholder="Type the English translation here...",
        key="vocab_answer"
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("✅ Check Answer", use_container_width=True, key="vocab_check"):
            if user_answer.strip().lower() in current_word['translation'].lower():
                st.success(f"🎉 Correct! '{current_word['word']}' means '{current_word['translation']}'")
                st.balloons()
            else:
                st.error(f"❌ Not quite. '{current_word['word']}' means '{current_word['translation']}'")
    
    with col2:
        if st.button("🔄 New Word", use_container_width=True, key="vocab_new"):
            st.session_state.current_vocab_word = random.choice(current_vocab)
            st.rerun()
    
    with col3:
        if st.button("💡 Show Answer", use_container_width=True, key="vocab_show"):
            st.info(f"**Answer:** {current_word['translation']}")
    
    st.session_state.show_vocab_quiz = False

if st.session_state.get("show_daily_practice"):
    language = st.session_state.get("current_language", "🇫🇷 French")
    level = st.session_state.get("current_level", "🌱 Beginner")
    
    # Daily practice questions based on language and level
    practice_questions = [
        f"Write a simple introduction in {language.split()[1]}",
        f"Describe your daily routine using {language.split()[1]} vocabulary",
        f"Create a dialogue between two people meeting for the first time",
        f"List 10 items you might find in a kitchen in {language.split()[1]}",
        f"Write about your favorite hobby using present tense verbs",
        f"Describe your family members in {language.split()[1]}",
        f"Plan a weekend trip using future tense",
        f"Write a restaurant conversation (ordering food)",
        f"Describe the weather in different seasons",
        f"Tell a story about your last vacation"
    ]
    
    # Select today's question
    if "daily_question" not in st.session_state:
        st.session_state.daily_question = random.choice(practice_questions)
    
    today_question = st.session_state.daily_question
    
    st.info(f"""
    **📝 Daily Practice - {language} ({level})**
    
    **Today's Challenge:**
    {today_question}
    
    **Difficulty Level**: {level.split()[1]}
    **Estimated Time**: 15 minutes
    
    💡 **Tip**: Try to answer without looking up the solution first!
    🎯 **Bonus**: Explain your answer aloud for speaking practice
    """)
    
    # Interactive Answer Section
    st.markdown("### ✍️ Your Answer")
    
    user_practice_answer = st.text_area(
        "Write your answer here:",
        height=100,
        placeholder="Type your response here...",
        key="practice_answer"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📨 Submit Answer", use_container_width=True, key="practice_submit"):
            if user_practice_answer.strip():
                st.success("🎉 Great job on completing today's practice!")
                st.info(f"""
                **Your Answer:**
                {user_practice_answer}
                
                **Next Steps:**
                • Review your answer with a native speaker if possible
                • Look up any words you weren't sure about
                • Practice speaking your answer out loud
                • Come back tomorrow for a new challenge!
                """)
                st.balloons()
    
    with col2:
        if st.button("🔄 New Question", use_container_width=True, key="practice_new"):
            st.session_state.daily_question = random.choice(practice_questions)
            st.rerun()
    
    st.session_state.show_daily_practice = False

if st.session_state.get("show_grammar"):
    language = st.session_state.get("current_language", "🇫🇷 French")
    level = st.session_state.get("current_level", "🌱 Beginner")
    
    st.info(f"""
    **📖 Grammar Lesson - {language} ({level})**
    
    **Today's Topic: Present Tense Verbs**
    
    **French Example:**
    • Je parle (I speak) - zhuh PARL
    • Tu parles (You speak) - too PARL
    • Il/Elle parle (He/She speaks) - eel/ell PARL
    
    **Pattern:** Most -er verbs follow this pattern
    
    **Practice:** Try conjugating "manger" (to eat)
    **Answer:** Je mange, Tu manges, Il/Elle mange
    
    🎯 **Tip**: Practice with regular verbs first, then learn irregular ones
    """)
    st.session_state.show_grammar = False

# Main chat interface
st.markdown("### 💬 Chat with FluentBot")

# Display chat history in a container
with st.container():
    if st.session_state.chat_history:
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="user-message">
                    👤 {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="assistant-message">
                    🤖 {message["content"]}
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="assistant-message">
            🤖 Hello! I'm FluentBot, your language learning companion. Select a language from the sidebar and let's start your learning journey! Ask me anything about grammar, vocabulary, or practice conversations.
        </div>
        """, unsafe_allow_html=True)

# Chat input
user_message = st.text_input(
    "Type your message here...",
    placeholder="Ask me about grammar, vocabulary, or start a conversation practice!",
    key="user_input"
)

if st.button("Send 📤", use_container_width=True, key="chat_send") or user_message:
    if user_message.strip():
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_message})
        
        # Get response based on current language learning context
        language_context = ""
        if "current_language" in st.session_state and "current_level" in st.session_state:
            lang = st.session_state.current_language
            level = st.session_state.current_level
            language_context = f"[Language Learning: {lang} - {level}] "
        
        # Get response - try backend first, fallback if issues
        if backend_available:
            try:
                with st.spinner("🤔 Thinking..."):
                    response = get_chat_response(user_message, st.session_state.chat_history[:-1], language_context)
            except Exception as e:
                st.error(f"Error: {str(e)}")
                response = "I apologize, but I'm having trouble connecting to the AI service. Please check your internet connection and try again."
        else:
            response = f"""🤖 **FluentBot - {language_context if language_context else 'General Chat'}**

I'm here to help you master languages! Here's what I can do:

**🗣️ Language Learning:**
• 30-day roadmaps for 20+ languages
• Daily practice with progressive difficulty
• Grammar explanations and vocabulary building
• Interactive conversation practice
• Cultural insights and practical usage tips

**🎯 Personalized Support:**
• Create custom study plans based on your goals
• Explain language concepts step-by-step
• Generate practice exercises and quizzes
• Provide pronunciation guides and memory techniques

Try asking me: "How do I say 'How are you?' in French?" or "Explain Spanish verb conjugations" or "Give me a conversation practice scenario!"
"""
        
        # Add assistant response to chat history
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        # Clear the input box
        st.session_state.user_input = ""
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem; opacity: 0.7;">
    <p>🤖 FluentBot - Your AI Language Learning Companion</p>
    <p>Master new languages with personalized AI assistance • 20+ Languages • Progressive Learning</p>
</div>
""", unsafe_allow_html=True)
