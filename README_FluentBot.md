# 🤖 FluentBot - AI-Powered Language Learning Platform

**FluentBot** is an intelligent language learning companion that helps you master 15+ languages through interactive AI-powered conversations, structured roadmaps, and engaging practice exercises.

![FluentBot](https://img.shields.io/badge/FluentBot-Language%20Learning-blue?style=for-the-badge&logo=robot)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Framework-red?style=for-the-badge&logo=streamlit)

## ✨ Features

### 🌍 **Multi-Language Support**
Support for 15+ languages including:
- 🇫🇷 **French** • 🇯🇵 **Japanese** • 🇩🇪 **German** • 🇪🇸 **Spanish**
- 🇮🇹 **Italian** • 🇰🇷 **Korean** • 🇨🇳 **Chinese** • 🇷🇺 **Russian**
- 🇵🇹 **Portuguese** • 🇳🇱 **Dutch** • 🇸🇦 **Arabic** • 🇮🇳 **Hindi**
- 🇸🇪 **Swedish** • 🇳🇴 **Norwegian** • 🇫🇮 **Finnish** • 🇵🇱 **Polish**
- 🇹🇷 **Turkish** • 🇬🇷 **Greek** • 🇮🇱 **Hebrew** • 🇻🇳 **Vietnamese** • 🇹🇭 **Thai**

### 🎯 **Learning Features**
- **📅 30-Day Roadmaps**: Structured learning plans for every language and skill level
- **🧠 Interactive Vocabulary Quizzes**: Learn new words with pronunciation guides
- **📝 Daily Practice**: Progressive exercises that adapt to your learning pace
- **💬 AI Chat Integration**: Practice conversations with FluentBot
- **🎚️ 4 Difficulty Levels**: Beginner → Elementary → Intermediate → Advanced
- **🎨 Dark Theme**: Professional ChatGPT-inspired interface

### 🚀 **AI-Powered Learning**
- **OpenRouter Integration**: Access to multiple AI models (GPT-4, Claude, Gemini)
- **Smart Conversations**: Context-aware responses for natural language practice
- **Personalized Learning**: Adapts to your progress and learning style
- **Cultural Context**: Learn language with cultural insights and practical usage

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenRouter API key (free at [openrouter.ai](https://openrouter.ai/))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/FluentBot.git
   cd FluentBot
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/Mac
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirement.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env file and add your API key
   # OPENROUTER_API_KEY=your_openrouter_api_key_here
   ```

5. **Run FluentBot**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser** to `http://localhost:8501`

## 🔑 API Configuration

### Required API Key

**OpenRouter** (Required)
- **Purpose**: AI chat functionality and language learning responses
- **Get your key**: [OpenRouter.ai](https://openrouter.ai/)
- **Setup**: Add `OPENROUTER_API_KEY=your_key_here` to `.env`
- **Models**: Access to GPT-4, Claude, Gemini, and more through one API

### Environment Setup

Create a `.env` file in the project root:

```bash
# FluentBot Environment Variables
# Only one API key needed - OpenRouter gives access to multiple AI models!

# OpenRouter API Key (Required - Get your free key from https://openrouter.ai/)
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

## 📱 Usage Guide

### 1. **Choose Your Language**
- Use the sidebar to select from 15+ supported languages
- Pick your current skill level (Beginner to Advanced)

### 2. **Start Learning**
- **📅 30-Day Roadmap**: Follow structured daily lessons
- **🧠 Vocabulary Quiz**: Test and learn new words
- **📝 Daily Practice**: Complete progressive exercises
- **💬 AI Chat**: Practice conversations in your target language

### 3. **Track Progress**
- Monitor your learning streak
- Complete daily challenges
- Advance through difficulty levels

## 🛠️ Technology Stack

### Core Framework
- **streamlit>=1.24.0**: Web application framework
- **python-dotenv>=1.0.0**: Environment variable management
- **requests>=2.31.0**: HTTP client for API communication

### AI Integration
- **openai>=1.0.0**: OpenRouter API client (compatible with OpenAI SDK)
- **OpenRouter**: Multi-model AI access (GPT-4, Claude, Gemini, etc.)

### Language Learning Features
- Interactive vocabulary system with pronunciation guides
- Progressive difficulty scaling
- Cultural context integration
- Real-time conversation practice

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Contribution Areas
- 🌍 Adding new languages
- 🎯 Improving learning algorithms
- 🎨 UI/UX enhancements
- 📚 Creating learning content
- 🐛 Bug fixes and optimizations

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenRouter** for providing access to multiple AI models
- **Streamlit** for the amazing web framework
- **The language learning community** for inspiration and feedback

## 📞 Support

Having issues? We're here to help:

- 🐛 **Bug Reports**: [Open an issue](https://github.com/your-username/FluentBot/issues)
- 💡 **Feature Requests**: [Suggest a feature](https://github.com/your-username/FluentBot/issues)
- 📧 **General Questions**: [Start a discussion](https://github.com/your-username/FluentBot/discussions)

---

**Start your language learning journey today with FluentBot!** 🚀🌍

*Made with ❤️ for language learners worldwide*
