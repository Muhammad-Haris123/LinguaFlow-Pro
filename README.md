# LinguaFlow Pro

A fast translation platform built with React and FastAPI, optimized for GPU acceleration. This project provides real-time translation services with a modern web interface.

## What it does

LinguaFlow Pro translates text between multiple languages using machine learning models. The backend runs on FastAPI with PyTorch for model inference, while the frontend is built with React and Tailwind CSS for a clean user experience.

## Features

- Real-time text translation
- Support for 12 languages including English, German, French, Spanish, and more
- GPU acceleration for faster processing
- Batch translation for CSV files
- Translation history and favorites
- Dark and light theme support
- Responsive design for mobile and desktop

## Requirements

- Python 3.8 or higher
- Node.js 16 or higher
- CUDA-compatible GPU (optional but recommended for better performance)
- Git

## Installation

### Backend Setup

1. Navigate to the project directory and create a virtual environment:
```bash
cd backend
python -m venv venv
```

2. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Start the FastAPI server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The application will be available at http://localhost:3000, with the API running on http://localhost:8000.

## Usage

1. Open the web interface in your browser
2. Select source and target languages from the dropdown menus
3. Type or paste text in the source text area
4. Click the Translate button to get the translation
5. Use the copy, share, or favorite buttons to manage translations

For batch processing, upload a CSV file with text to translate multiple entries at once.

## API Endpoints

- `GET /health` - Check if the service is running
- `POST /translate` - Translate text from one language to another
- `GET /languages` - Get list of supported languages
- `GET /stats` - Get API usage statistics

Example translation request:
```bash
curl -X POST "http://localhost:8000/translate" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "Hello world",
       "source_language": "en",
       "target_language": "de"
     }'
```

## Supported Languages

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

## Performance

With GPU acceleration, translations typically complete in 1-2 seconds. On CPU-only systems, expect 3-5 seconds per translation. Repeated translations are cached for faster response times.

## Project Structure

```
linguaflow-pro/
├── backend/           # FastAPI application
│   ├── main.py       # Main server file
│   └── requirements.txt
├── frontend/         # React application
│   ├── src/
│   │   ├── App.js    # Main component
│   │   └── App.css   # Styles
│   └── package.json
├── docs/            # Documentation
└── tests/           # Test files
```

## Configuration

The application uses environment variables for configuration:

- `CUDA_VISIBLE_DEVICES` - GPU device selection
- `REDIS_URL` - Redis cache connection
- `MODEL_PATH` - Custom model directory

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Troubleshooting

If you encounter issues:

1. Make sure all dependencies are installed correctly
2. Check that Python and Node.js versions meet requirements
3. Verify GPU drivers are installed if using CUDA acceleration
4. Check the console for error messages

For persistent issues, please open an issue on GitHub with details about your setup and the error messages you're seeing.
