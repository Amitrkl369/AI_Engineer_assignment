# Marksheet Extractor

An AI-powered web application that extracts structured data from marksheet documents using OCR and LLM processing.

## Features

- 📄 **Document Processing**: Supports PDF and image formats (PNG, JPG, JPEG)
- 🤖 **AI-Powered Extraction**: Uses Tesseract OCR + OpenAI GPT for accurate data extraction
- 🎯 **Confidence Scoring**: Dual confidence system combining OCR and LLM scores
- 🎨 **Interactive Frontend**: Modern, animated web interface for easy data review and editing
- 📊 **Structured Output**: JSON output with candidate info, subjects, and metadata
- 🚀 **FastAPI Backend**: High-performance REST API with automatic documentation

## Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/Amitrkl369/AI_Engineer_assignment.git
   cd marksheet-extractor
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # or
   source .venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI API key
   ```

5. **Run the application**
   ```bash
   python app/main.py
   ```

6. **Access the application**
   - API: http://localhost:8000
   - Interactive Frontend: http://localhost:8000/frontend
   - API Documentation: http://localhost:8000/docs

## API Usage

### Extract Marksheet Data

```bash
curl -X POST "http://localhost:8000/api/v1/extract" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@marksheet.pdf"
```

**Response Format:**
```json
{
  "candidate": {
    "name": {"value": "John Doe"},
    "roll_no": {"value": "12345"},
    "father_name": {"value": "Jane Doe"},
    // ... other fields
  },
  "subjects": [
    {
      "subject": {"value": "Mathematics"},
      "max_marks": {"value": "100"},
      "obtained_marks": {"value": "95"},
      "grade": {"value": "A"}
    }
  ],
  "overall_result": {"value": "First Division"},
  "confidence_explanation": "..."
}
```

## Deployment

### Railway (Recommended)

1. **Connect GitHub Repository**
   - Go to [Railway.app](https://railway.app)
   - Connect your GitHub account
   - Select the `AI_Engineer_assignment` repository

2. **Configure Environment**
   - Add environment variable: `OPENAI_API_KEY`
   - Railway will automatically detect Python and install dependencies

3. **Deploy**
   - Railway will build and deploy automatically
   - Get your public URL from the Railway dashboard

### Render

1. **Go to [Render.com](https://render.com)** and create a free account
2. **Create a new Web Service** and connect your GitHub repo
3. **Configure build settings**:
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app/main.py`
4. **Add environment variable**: `OPENAI_API_KEY`
5. **Deploy**

### Vercel (Not Recommended)

⚠️ **Note**: Vercel is primarily designed for frontend apps and serverless functions. This FastAPI app may not work optimally due to:
- File upload limitations
- Execution time limits
- Serverless function constraints

If you still want to try:

1. **Go to [Vercel.com](https://vercel.com)** and connect your GitHub repo
2. **Add environment variable**: `OPENAI_API_KEY`
3. **Deploy** (Vercel will use the `vercel.json` configuration)

### Manual Deployment

For other platforms (Heroku, etc.):

1. **Install system dependencies** (for Tesseract OCR)
   ```bash
   # Ubuntu/Debian
   sudo apt-get install tesseract-ocr tesseract-ocr-eng

   # macOS
   brew install tesseract

   # Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
   ```

2. **Set environment variables**
   ```bash
   OPENAI_API_KEY=your_api_key_here
   ```

3. **Run with production server**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

## Project Structure

```
marksheet-extractor/
├── app/
│   ├── api/v1/
│   │   ├── __init__.py
│   │   └── extract.py          # API endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py           # Configuration
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py          # Pydantic models
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ocr.py             # OCR processing
│   │   └── llm.py             # LLM processing
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── confidence.py      # Confidence calculation
│   │   └── file_utils.py      # File utilities
│   └── main.py                # FastAPI application
├── frontend_interactive.html  # Interactive web interface
├── requirements.txt           # Python dependencies
├── .env.example              # Environment template
├── .gitignore               # Git ignore rules
├── APPROACH.md              # Technical approach documentation
└── README.md                # This file
```

## Technology Stack

- **Backend**: FastAPI, Python 3.11+
- **OCR**: Tesseract OCR, pdf2image
- **AI**: OpenAI GPT-4
- **Frontend**: HTML5, CSS3, JavaScript
- **Deployment**: Railway (recommended)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
