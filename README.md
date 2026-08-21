# 🤖 Conspiracy Chat Bot

**Author:** Jimbo

A lightweight, multi-interface chatbot featuring **iterative reasoning** (initial answer → critique → final answer) with support for OpenAI, Anthropic, and local LLaMA backends.

## Features

✅ **Three Interfaces:**
- FastAPI Web UI (`http://localhost:8000/ui`)
- Streamlit App (`streamlit run streamlit_app.py`)
- CLI (`python main.py think "Your question"`)

✅ **Iterative Reasoning:**
- Initial response with step-by-step reasoning
- AI critique of its own answer
- Refined final answer addressing critique

✅ **Multi-Backend Support:**
- OpenAI (GPT-4o-mini, etc.)
- Anthropic (Claude)
- Local LLaMA (via llama-cpp-python)

✅ **Production Ready:**
- Error handling & logging
- Docker support
- Environment variable configuration
- Type hints & documentation

---

## Quick Start

### 1. Install Dependencies

```bash
# Option A: Using uv (recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync

# Option B: Using pip
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your API keys:
# - OPENAI_API_KEY (required for OpenAI backend)
# - ANTHROPIC_API_KEY (required for Anthropic backend)
# - LLAMA_MODEL_PATH (required for local LLaMA backend)
```

### 3. Run the App

#### **FastAPI Web Server** (Recommended)
```bash
python main.py serve
# Open http://localhost:8000/ui in your browser
```

#### **Streamlit App**
```bash
streamlit run streamlit_app.py
# Opens in your browser automatically
```

#### **CLI**
```bash
python main.py think "Explain quantum entanglement"
python main.py think "What is machine learning?" --backend openai --no-steps
```

#### **Start Interactive CLI**
```bash
python main.py greet Jimbo
```

---

## API Endpoints

### `GET /`
Health check
```bash
curl http://localhost:8000/
```

### `GET /ui`
Interactive web UI
```bash
open http://localhost:8000/ui
```

### `POST /think`
Submit a question for reasoning
```bash
curl -X POST http://localhost:8000/think \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is machine learning?",
    "backend": "openai",
    "show_steps": true
  }'
```

**Response:**
```json
{
  "initial": "Machine learning is a subset of artificial intelligence...",
  "critique": "The above answer is somewhat vague...",
  "final": "Machine learning is a field of AI that..."
}
```

---

## Docker

### Build & Run
```bash
docker build -t conspiracy-bot .
docker run -p 8000:8000 \
  -e OPENAI_API_KEY="your_key_here" \
  conspiracy-bot
```

### With .env file
```bash
docker run -p 8000:8000 --env-file .env conspiracy-bot
```

---

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# OpenAI (required if using openai backend)
OPENAI_API_KEY=sk-...

# Anthropic (required if using anthropic backend)
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-3-opus-20240229  # Optional, defaults to claude-3-opus

# Local LLaMA (required if using llama backend)
LLAMA_MODEL_PATH=/path/to/model.gguf
```

### Supported Models

| Backend | Models |
|---------|--------|
| **OpenAI** | gpt-4, gpt-4o, gpt-4o-mini, gpt-3.5-turbo |
| **Anthropic** | claude-3-opus, claude-3-sonnet, claude-3-haiku |
| **LLaMA** | Any GGUF format model (Mistral, Llama, etc.) |

---

## Project Structure

```
conspiracy.chat.bot/
├── main.py                 # FastAPI + CLI app
├── reasoning_iter.py       # Core iterative reasoning logic
├── streamlit_app.py        # Streamlit UI
├── requirements.txt        # Dependencies
├── pyproject.toml         # Project metadata
├── .env.example           # Environment template
├── Dockerfile             # Docker configuration
├── Procfile               # Heroku deployment
└── README.md              # This file
```

---

## Development

### Add New Backend

1. Create a `_call_<backend>()` function in `reasoning_iter.py`
2. Update `_backend_call()` to route to it
3. Add environment variables to `.env.example`
4. Update documentation above

### Logging

Logs are sent to console. For file logging, modify:

```python
# In main.py or streamlit_app.py
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

---

## Troubleshooting

### "OPENAI_API_KEY not set"
- Create `.env` file with your key
- Run: `export OPENAI_API_KEY="sk-..."` (Linux/Mac) or `set OPENAI_API_KEY=sk-...` (Windows)

### Streamlit not starting
```bash
pip install --upgrade streamlit
streamlit run streamlit_app.py --logger.level=debug
```

### FastAPI not responding
```bash
python main.py serve --host 0.0.0.0 --port 8000
# Then visit http://localhost:8000/ui
```

### Package import errors
```bash
pip install -r requirements.txt --force-reinstall
```

---

## Performance Tips

- Use `gpt-4o-mini` for fast, cheaper responses
- Use `gpt-4` for complex reasoning tasks
- Anthropic's Claude is often more creative
- Local LLaMA is privacy-preserving but slower

---

## License

Apache License 2.0 — See LICENSE file

---

**Author:** Jimbo  
**Last Updated:** 2024
