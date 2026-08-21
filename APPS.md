# 🚀 Conspiracy Chat Bot Suite

## Available Apps

### 1. **🤖 Conspiracy Chat Bot**
**Iterative Reasoning Chatbot with Multiple Backend Support**

- **URL**: `http://localhost:8000/ui`
- **Launch**: `python launch.py chatbot`
- **Features**:
  - Iterative reasoning: Initial → Critique → Final
  - Backend options: OpenAI, Anthropic, LLaMA
  - API endpoint: `POST /think`
  - CLI support: `python main.py think "Your question"`
  - Beautiful gradient UI

**API Examples**:
```bash
# Using cURL
curl -X POST http://localhost:8000/think \
  -H "Content-Type: application/json" \
  -d '{"question": "What is quantum physics?", "backend": "openai", "show_steps": true}'

# Using Python
import requests
response = requests.post(
    'http://localhost:8000/think',
    json={
        'question': 'Explain machine learning',
        'backend': 'openai',
        'show_steps': True
    }
)
print(response.json())
```

---

### 2. **⏰ Digital Clock**
**Real-time World Clock with Multiple Time Zones**

- **URL**: `http://localhost:8001/ui`
- **Launch**: `python launch.py clock`
- **Features**:
  - 15 major cities worldwide
  - 24-hour and 12-hour format toggle
  - UTC offsets displayed
  - Auto-update every second
  - Beautiful glass-morphism design
  - API endpoint: `GET /api/time`

**Supported Cities**:
- New York (America/New_York)
- Los Angeles (America/Los_Angeles)
- London (Europe/London)
- Paris (Europe/Paris)
- Tokyo (Asia/Tokyo)
- Sydney (Australia/Sydney)
- Dubai (Asia/Dubai)
- Singapore (Asia/Singapore)
- Hong Kong (Asia/Hong_Kong)
- Mumbai (Asia/Kolkata)
- Bangkok (Asia/Bangkok)
- Istanbul (Europe/Istanbul)
- São Paulo (America/Sao_Paulo)
- Mexico City (America/Mexico_City)
- Toronto (America/Toronto)

**API Examples**:
```bash
# Get current time in all zones
curl http://localhost:8001/api/time

# Response example:
{
  "New York": {
    "time": "14:30:45",
    "date": "2024-08-21",
    "timezone": "America/New_York",
    "utc_offset": "-0400",
    "12h_format": "02:30:45 PM"
  },
  ...
}
```

---

### 3. **🎨 Conspiracy Chat Bot (Streamlit)**
**Beautiful Streamlit Interface for Conspiracy Chat Bot**

- **Launch**: `python launch.py streamlit_chat`
- **Features**:
  - Modern gradient UI
  - Sidebar configuration
  - Backend status indicator
  - Step-by-step output display
  - Beautiful formatting
  - Error handling with emoji indicators

---

## Quick Start

### Option 1: Interactive Menu
```bash
python launch.py menu
```
Then select which app to run!

### Option 2: Direct Launch
```bash
# Conspiracy Chat Bot (FastAPI)
python launch.py chatbot

# Digital Clock
python launch.py clock

# Conspiracy Chat Bot (Streamlit)
python launch.py streamlit_chat
```

### Option 3: List Available Apps
```bash
python launch.py list-apps
```

---

## Environment Configuration

Create a `.env` file in the project root:

```env
# For Conspiracy Chat Bot
OPENAI_API_KEY=sk-your-key
ANTHROPIC_API_KEY=sk-ant-your-key
ANTHROPIC_MODEL=claude-3-opus-20240229
LLAMA_MODEL_PATH=/path/to/model.gguf
```

---

## Running Multiple Apps Simultaneously

You can run multiple apps at the same time (in different terminals):

```bash
# Terminal 1: Conspiracy Chat Bot
python launch.py chatbot

# Terminal 2: Digital Clock
python launch.py clock --port 8001

# Terminal 3: Streamlit Chat Bot
python launch.py streamlit_chat
```

Then access:
- Conspiracy Chat Bot: `http://localhost:8000/ui`
- Digital Clock: `http://localhost:8001/ui`
- Streamlit App: `http://localhost:8501`

---

## Deployment

Both apps are ready to deploy on Railway, Docker, or your own server!

See `DEPLOYMENT.md` for detailed instructions.

---

## Author
**Jimbo**

🎉 Enjoy your app suite!
