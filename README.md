# 🎓 StudyMate AI

A modern, AI-powered study companion built with Streamlit. Features a beautiful dark theme inspired by ChatGPT and multiple AI model integrations for comprehensive study assistance.

![StudyMate AI](https://img.shields.io/badge/StudyMate-AI%20Powered-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.24+-red)

## ✨ Features

### 🎨 Modern UI/UX
- **Dark Theme**: ChatGPT-inspired design with modern aesthetics
- **Responsive Layout**: Clean, professional interface
- **Smooth Animations**: Hover effects and transitions
- **Accessibility**: Proper contrast and readable fonts

### 🤖 AI-Powered Chat
- **Multiple AI Models**: Access to various models through OpenRouter
- **Intelligent Fallbacks**: OpenRouter → Gemini → Enhanced offline responses
- **Study-Focused**: Specialized prompts for educational content
- **Context Awareness**: Maintains conversation history

### 📚 Study Tools
- **Study Modes**: Focus areas (Math & Science, Languages, History, Test Prep, Research)
- **Pomodoro Timer**: Built-in focus timer with visual countdown
- **Quick Help**: Study tips, memory techniques, and progress tracking
- **Example Questions**: Ready-to-use conversation starters

### 🔒 Security
- **Environment Variables**: Secure API key management
- **No Exposed Keys**: All sensitive data properly protected
- **Clean Codebase**: No hardcoded credentials

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ashutosh8021/study-chatbot.git
   cd study-chatbot
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv .venv
   
   # On Windows
   .venv\Scripts\activate
   
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirement.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env file and add your API keys
   # At minimum, you need OPENROUTER_API_KEY
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open in browser**
   - Local: http://localhost:8501
   - Network: http://your-ip:8501

## 🔧 Configuration

### Required API Keys

#### OpenRouter API (Primary)
- **Get your key**: [OpenRouter.ai](https://openrouter.ai/)
- **Purpose**: Access to multiple AI models (GPT, Claude, Llama, etc.)
- **Setup**: Add `OPENROUTER_API_KEY=your_key_here` to `.env`

### Optional API Keys

#### Google Gemini (Fallback)
- **Get your key**: [Google AI Studio](https://aistudio.google.com/)
- **Purpose**: Fallback AI model
- **Setup**: Add `GEMINI_API_KEY=your_key_here` to `.env`

#### Hugging Face (Additional Fallback)
- **Get your token**: [Hugging Face Settings](https://huggingface.co/settings/tokens)
- **Purpose**: Additional fallback option
- **Setup**: Add `HF_API_TOKEN=your_token_here` to `.env`

### Environment Variables
Create a `.env` file in the project root:

```env
# Required
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Optional
GEMINI_API_KEY=your_gemini_api_key_here
HF_API_TOKEN=your_huggingface_token_here
OPENAI_API_KEY=your_openai_api_key_here
```

## 📖 Usage

### Study Modes
Choose from specialized study areas:
- **General Study**: Broad academic assistance
- **Math & Science**: Problem-solving and concept explanation
- **Languages**: Grammar, writing, and language learning
- **History**: Historical events and analysis
- **Test Prep**: Exam strategies and review
- **Research Help**: Research methods and citation

### Focus Timer
- Set study sessions from 5-120 minutes
- Visual countdown with notifications
- Pomodoro technique support
- Session completion celebrations

### Quick Help Features
- **Study Tips**: Effective learning strategies
- **Memory Tips**: Memory enhancement techniques
- **Progress Tracking**: Session statistics and insights

### Example Interactions
- "Can you explain basic statistics concepts like mean, median, and standard deviation?"
- "Help me create an effective study schedule for my exams"
- "Suggest some simple chemistry experiments I can do at home"
- "What's the best way to memorize historical dates?"

## 🛠️ Technical Details

### Architecture
- **Frontend**: Streamlit with custom CSS
- **Backend**: Python with multiple API integrations
- **AI Models**: OpenRouter (primary), Gemini (fallback), enhanced offline responses
- **State Management**: Streamlit session state

### File Structure
```
study-chatbot/
├── app.py              # Main Streamlit application
├── backend.py          # AI API integrations and response handling
├── requirement.txt     # Python dependencies
├── .env.example        # Environment variables template
├── .gitignore         # Git ignore rules
└── README.md          # Project documentation
```

### Dependencies
- **streamlit>=1.24.0**: Web application framework
- **openai>=1.0.0**: OpenAI API client (for OpenRouter compatibility)
- **requests>=2.25.0**: HTTP library for API calls
- **google-generativeai>=0.3.0**: Google Gemini API client

## 🎨 Customization

### Themes
The app uses a dark theme by default. To modify:
1. Edit the CSS in `app.py`
2. Modify color variables for different schemes
3. Adjust fonts and spacing as needed

### AI Models
To change the AI model used by OpenRouter:
1. Open `backend.py`
2. Modify the `model` parameter in the `get_openrouter_response` function
3. Choose from available models on OpenRouter

### Study Modes
To add new study modes:
1. Edit the selectbox options in `app.py`
2. Add corresponding logic in the message handling
3. Update the backend prompt engineering as needed

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **Streamlit** for the excellent web app framework
- **OpenRouter** for providing access to multiple AI models
- **Google** for the Gemini API
- **Hugging Face** for additional AI model access

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/ashutosh8021/study-chatbot/issues) page
2. Create a new issue if your problem isn't already reported
3. Provide detailed information about your setup and the issue

## 🔮 Future Enhancements

- [ ] User authentication and profiles
- [ ] Study progress analytics
- [ ] Flashcard system
- [ ] File upload and analysis
- [ ] Voice interaction support
- [ ] Mobile app version
- [ ] Collaborative study rooms
- [ ] Integration with learning management systems

---

**Made with ❤️ for students everywhere**

*StudyMate AI - Empowering Your Learning Journey* 🎓
