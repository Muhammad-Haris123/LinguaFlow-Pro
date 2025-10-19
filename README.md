# 🌐 LinguaFlow Pro - Enterprise Translation Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/React-18.0+-61dafb.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com/)

> **Ultra-fast GPU-optimized translation platform powered by RTX 5060 Ti. Sub-2-second responses with enterprise-grade reliability.**

## ✨ Features

- 🚀 **GPU-Accelerated**: Optimized for RTX 5060 Ti with CUDA support
- ⚡ **Ultra-Fast**: Sub-2-second translation responses
- 🌍 **Multi-Language**: Support for 12+ languages
- 🎨 **Modern UI**: Beautiful React frontend with Tailwind CSS
- 🔒 **Enterprise-Ready**: Professional-grade security and reliability
- 📊 **Analytics**: Usage tracking and performance metrics
- 🎯 **Batch Processing**: Upload CSV files for bulk translation
- 🌙 **Dark/Light Mode**: Beautiful theme switching

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PyTorch** - Deep learning framework
- **Transformers** - Hugging Face model library
- **CUDA** - GPU acceleration
- **Redis** - Caching layer

### Frontend
- **React 18** - Modern UI framework
- **Tailwind CSS** - Utility-first CSS
- **Framer Motion** - Smooth animations
- **Lucide React** - Beautiful icons

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- CUDA-compatible GPU (optional but recommended)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/linguaflow-pro.git
   cd linguaflow-pro
   ```

2. **Backend Setup**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # Windows
   venv\\Scripts\\activate
   # macOS/Linux
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Start backend server
   cd backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Frontend Setup**
   ```bash
   # Install dependencies
   cd frontend
   npm install
   
   # Start development server
   npm start
   ```

4. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## 📖 API Documentation

### Endpoints

- `GET /health` - Health check
- `POST /translate` - Translate text
- `GET /languages` - Get supported languages
- `GET /stats` - Get API statistics

### Example Translation Request

```bash
curl -X POST "http://localhost:8000/translate" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "Hello, world!",
       "source_language": "en",
       "target_language": "de",
       "max_length": 50
     }'
```

## 🎯 Performance

- **GPU Mode**: 1-2 seconds per translation
- **CPU Mode**: 3-5 seconds per translation
- **Cached**: <0.1 seconds for repeated translations
- **Batch**: 100+ translations per minute

## 🌍 Supported Languages

- English (en)
- German (de)
- French (fr)
- Spanish (es)
- Italian (it)
- Portuguese (pt)
- Russian (ru)
- Japanese (ja)
- Korean (ko)
- Chinese (zh)
- Arabic (ar)
- Hindi (hi)

## 🔧 Configuration

### Environment Variables

```bash
# Backend
CUDA_VISIBLE_DEVICES=0  # GPU device
REDIS_URL=redis://localhost:6379  # Redis cache
MODEL_PATH=trained_translation_model  # Custom model path

# Frontend
REACT_APP_API_URL=http://localhost:8000  # Backend URL
```

## 📊 Project Structure

```
linguaflow-pro/
├── backend/                 # FastAPI backend
│   ├── main.py             # Main application
│   ├── requirements.txt    # Python dependencies
│   └── trained_translation_model/  # Model files
├── frontend/               # React frontend
│   ├── src/
│   │   ├── App.js         # Main component
│   │   ├── App.css        # Styles
│   │   └── components/    # UI components
│   ├── package.json       # Node dependencies
│   └── tailwind.config.js # Tailwind config
├── docs/                  # Documentation
├── tests/                 # Test files
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Hugging Face Transformers](https://huggingface.co/transformers/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://reactjs.org/)
- [Tailwind CSS](https://tailwindcss.com/)

## 📞 Support

- 📧 Email: support@linguaflow-pro.com
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/linguaflow-pro/issues)
- 📖 Docs: [Documentation](https://docs.linguaflow-pro.com)

---

**Made with ❤️ by the LinguaFlow Pro Team**