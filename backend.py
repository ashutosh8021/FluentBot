from typing import List, Dict
import requests
import json
import os

class FluentBotBackend:
    def __init__(self):
        # API Keys from environment variables
        self.openrouter_key = os.environ.get("OPENROUTER_API_KEY", "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")
        self.gemini_key = os.environ.get("GEMINI_API_KEY", "AIzaSyAQ-eDivuDXmF2XoKdla7k-pzCCxl6cuts")
        
        # API endpoints
        self.openrouter_url = "https://openrouter.ai/api/v1/chat/completions"
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={self.gemini_key}"
        
        # Enhanced system prompt for FluentBot - Language Learning Focus
        self.system_prompt = """You are FluentBot, an advanced AI language learning companion designed to help users master new languages effectively. Your personality is:

� **Language Expert**: You have deep knowledge across 20+ languages and proven teaching methodologies
📚 **Supportive**: Always encouraging, patient, and motivating in language learning journey
🧠 **Adaptive**: Adjust your teaching style based on the learner's level and learning preferences
✨ **Creative**: Use cultural context, real-life examples, and engaging explanations to make language learning fun
� **Results-Focused**: Help learners achieve measurable progress through structured practice

**Your Core Functions:**
• Explain grammar rules clearly with practical examples
• Provide vocabulary building strategies and mnemonics
• Create interactive practice exercises and conversation starters
• Help with pronunciation through phonetic guidance
• Offer cultural insights and context for authentic language use
• Suggest immersive learning techniques and resources
• Support language certification exam preparation

**🌍 Language Learning Expertise:**
• Create personalized 30-day learning roadmaps for any language
• Design daily practice exercises with progressive difficulty
• Provide vocabulary quizzes and memory techniques
• Explain grammar rules with clear examples and exceptions
• Offer cultural context and practical usage tips
• Support all levels: Beginner → Elementary → Intermediate → Advanced
• Generate conversation practice scenarios
• Create pronunciation guides and phonetic breakdowns
• Design writing exercises and correction feedback
• Recommend authentic materials (books, movies, music) for each level

**Supported Languages Include:**
French, Japanese, German, Spanish, Italian, Korean, Chinese (Mandarin), Russian, Portuguese, Dutch, Arabic, Hindi, Swedish, Norwegian, Finnish, Polish, Turkish, Greek, Hebrew, Vietnamese, Thai, and more.

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

backend = FluentBotBackend()

def get_chat_response(user_input: str, chat_history: List[Dict] = None, language_context: str = "") -> str:
    """
    Get AI response using multiple API providers with fallback system
    """
    if chat_history is None:
        chat_history = []
    
    # Add language learning context to the prompt
    context_prompt = f"{language_context}{user_input}" if language_context else user_input
    
    # Try OpenRouter first (primary AI service)
    try:
        response = get_openrouter_response(context_prompt, chat_history)
        if response and len(response.strip()) > 10:
            return response
    except Exception as e:
        print(f"OpenRouter failed: {e}")
    
    # Try Google Gemini as fallback
    try:
        response = get_gemini_response(context_prompt)
        if response and len(response.strip()) > 10:
            return response
    except Exception as e:
        print(f"Gemini failed: {e}")
    
    # Enhanced offline fallback
    return get_enhanced_fallback_response(user_input, language_context)

def get_openrouter_response(user_input: str, chat_history: List[Dict] = None) -> str:
    """
    Get response from OpenRouter API (supports multiple AI models)
    """
    if chat_history is None:
        chat_history = []
    
    # Prepare messages
    messages = [{"role": "system", "content": backend.system_prompt}]
    
    # Add recent chat history (last 10 messages for context)
    for msg in chat_history[-10:]:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })
    
    # Add current user message
    messages.append({"role": "user", "content": user_input})
    
    headers = {
        "Authorization": f"Bearer {backend.openrouter_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://fluentbot-ai.streamlit.app",
        "X-Title": "FluentBot"
    }
    
    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": messages,
        "max_tokens": 1000,
        "temperature": 0.7,
        "top_p": 0.9
    }
    
    response = requests.post(backend.openrouter_url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    
    result = response.json()
    return result['choices'][0]['message']['content'].strip()

def get_gemini_response(user_input: str) -> str:
    """
    Get response from Google Gemini API
    """
    context = backend.system_prompt + "\n\n"
    full_prompt = context + f"Student: {user_input}\nFluentBot:"
    
    payload = {
        "contents": [{
            "parts": [{
                "text": full_prompt
            }]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "topK": 40,
            "topP": 0.95,
            "maxOutputTokens": 1000
        }
    }
    
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(backend.gemini_url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    
    result = response.json()
    
    if 'candidates' in result and len(result['candidates']) > 0:
        return result['candidates'][0]['content']['parts'][0]['text'].strip()
    
    raise Exception("No valid response from Gemini")

def get_enhanced_fallback_response(user_input: str, language_context: str = "") -> str:
    """
    Enhanced offline fallback responses for when APIs are unavailable
    """
    user_lower = user_input.lower()
    
    # Language learning responses
    if any(word in user_lower for word in ['language', 'french', 'japanese', 'german', 'spanish', 'italian', 'korean', 'chinese', 'russian', 'portuguese', 'dutch']):
        return """🌍 **Language Learning with StudyMate AI**

I'm excited to help you learn a new language! Here's how I can assist:

**📅 30-Day Roadmaps**: Structured learning plans for any language
**📝 Daily Practice**: Progressive exercises that increase in difficulty
**🧠 Vocabulary Building**: Memory techniques and spaced repetition
**📖 Grammar Lessons**: Clear explanations with practical examples
**🗣️ Conversation Practice**: Realistic scenarios and dialogues
**🎯 Level Progression**: Beginner → Elementary → Intermediate → Advanced

**Supported Languages:**
🇫🇷 French • 🇯🇵 Japanese • 🇩🇪 German • 🇪🇸 Spanish • 🇮🇹 Italian • 🇰🇷 Korean
🇨🇳 Chinese • 🇷🇺 Russian • 🇵🇹 Portuguese • 🇳🇱 Dutch • And many more!

**What would you like to learn?**
- "Create a 30-day French roadmap for beginners"
- "Give me daily Japanese practice exercises"
- "Explain German grammar rules"
- "Help me practice Spanish conversation"

Use the Language Learning panel in the sidebar for structured lessons, or ask me specific questions about any language! 🚀"""

    # Study tips
    elif any(word in user_lower for word in ['study', 'learn', 'remember', 'memorize', 'tips']):
        return """📚 **Effective Study Strategies**

**🧠 Active Learning Techniques:**
• **Pomodoro Technique**: 25 min study + 5 min break
• **Active Recall**: Test yourself instead of re-reading
• **Spaced Repetition**: Review at increasing intervals
• **Feynman Technique**: Explain concepts in simple terms

**💡 Memory Enhancement:**
• **Mnemonics**: Create memorable acronyms or phrases
• **Mind Maps**: Visual connections between concepts
• **Story Method**: Turn facts into memorable narratives
• **Method of Loci**: Associate information with familiar places

**📖 Subject-Specific Tips:**
• **Math/Science**: Practice problems, understand concepts before memorizing
• **Languages**: Immersion, daily practice, focus on communication
• **History**: Timeline creation, cause-and-effect analysis
• **Literature**: Active reading, character analysis, theme identification

**⏰ Time Management:**
• Set specific, achievable goals for each session
• Use a study schedule and stick to it
• Eliminate distractions (phone, social media)
• Track your progress and celebrate small wins

What specific subject or study challenge would you like help with?"""

    # Math help
    elif any(word in user_lower for word in ['math', 'algebra', 'calculus', 'geometry', 'statistics']):
        return """🔢 **Mathematics Study Guide**

**🎯 Math Learning Strategies:**
• **Understand Before Memorizing**: Focus on concepts, not just formulas
• **Practice Regularly**: Work through problems daily
• **Show All Work**: Step-by-step solutions help identify mistakes
• **Check Your Answers**: Substitute back into original equations
• **Use Visual Aids**: Graphs, diagrams, and charts

**📊 By Subject:**
• **Algebra**: Master basics, practice factoring, solve systems
• **Geometry**: Draw diagrams, learn proofs, use coordinate geometry
• **Calculus**: Understand limits, practice derivatives and integrals
• **Statistics**: Learn distributions, hypothesis testing, data analysis

**🔧 Problem-Solving Steps:**
1. Read the problem carefully
2. Identify what you're looking for
3. Determine what information you have
4. Choose the appropriate method/formula
5. Solve step by step
6. Check your answer

**💡 Math Study Tips:**
• Form study groups to discuss problems
• Teach concepts to others
• Use online tools for visualization
• Connect math to real-world applications

What specific math topic would you like help with?"""

    # General encouragement
    else:
        context_display = language_context.strip() if language_context else "General Chat"
        return f"""� **LinguaChat AI - {context_display}**

I'm here to help you master languages! Here's what I can do:

**�️ Language Learning:**
• 30-day roadmaps for 20+ languages
• Daily practice with progressive difficulty
• Grammar explanations and vocabulary building
• Interactive conversation practice
• Cultural insights and practical usage tips

**� Personalized Support:**
• Create custom study plans based on your goals
• Explain language concepts step-by-step
• Generate practice exercises and quizzes
• Provide pronunciation guides and memory techniques
• Cultural context and practical usage

**🔬 Subject Expertise:**
• Mathematics and Sciences
• Literature and Writing
• History and Social Studies
• Test preparation strategies

**⚡ Quick Features:**
• Focus timer for study sessions
• Study mode selection for specialized help
• Progress tracking and motivation
• Immediate answers to your questions

**To get started, try asking:**
• "Help me understand calculus derivatives"
• "Create a French study plan for beginners"
• "Give me practice questions for biology"
• "How can I improve my essay writing?"

What would you like to learn about today? 🌟"""
