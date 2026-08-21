# 🎯 Quick Reference

## Launch Apps

```bash
# Interactive menu (recommended)
python launch.py menu

# Or direct commands:
python launch.py chatbot         # Conspiracy Chat Bot
python launch.py clock           # Digital Clock
python launch.py streamlit_chat  # Streamlit version
```

## URLs

| App | URL | Port |
|-----|-----|------|
| 🤖 Chat Bot (FastAPI) | http://localhost:8000/ui | 8000 |
| ⏰ Digital Clock | http://localhost:8001/ui | 8001 |
| 🎨 Chat Bot (Streamlit) | http://localhost:8501 | 8501 |

## API Endpoints

### Conspiracy Chat Bot
- `GET /` - Health check
- `GET /ui` - Web UI
- `POST /think` - Submit reasoning request
- `GET /docs` - API documentation

### Digital Clock
- `GET /` - Health check
- `GET /ui` - Clock UI
- `GET /api/time` - Get all times

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create .env file
cp .env.example .env
# Edit .env and add your API keys

# 3. Run!
python launch.py menu
```

## Author
**Jimbo** 🎉
