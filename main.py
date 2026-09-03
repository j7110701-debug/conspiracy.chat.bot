# main.py
# Author: Jimbo
# Conspiracy Chat Bot — lightweight FastAPI + CLI app with iterative reasoning

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import click
import uvicorn
from pydantic import BaseModel
from typing import Optional
import os
import logging
from dotenv import load_dotenv

import reasoning_iter as reasoning

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Conspiracy Chat Bot",
    description="Iterative-reasoning assistant with multi-backend support (author: Jimbo)",
    version="1.0.0"
)

# Add CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    """Health check endpoint."""
    return {
        "message": "🤖 Conspiracy Chat Bot is running!",
        "author": "Jimbo",
        "endpoints": {
            "ui": "GET /ui",
            "api": "POST /think",
            "docs": "GET /docs"
        }
    }


class ThinkRequest(BaseModel):
    """Request schema for the /think endpoint."""
    question: str
    backend: Optional[str] = "openai"  # openai | anthropic | llama
    show_steps: Optional[bool] = True


@app.post("/think")
def think(req: ThinkRequest):
    """Endpoint to run iterative refinement reasoning using specified backend."""
    try:
        logger.info(f"Received reasoning request: backend={req.backend}, show_steps={req.show_steps}")
        result = reasoning.iterative_refine(
            req.question,
            backend=req.backend,
            show_steps=req.show_steps
        )
        return JSONResponse(content=result)
    except Exception as e:
        logger.error(f"Error in /think endpoint: {e}")
        return JSONResponse(
            status_code=400,
            content={"error": str(e)}
        )


@app.get("/ui", response_class=HTMLResponse)
async def ui(request: Request):
    """Simple interactive UI for the chatbot."""
    html = f"""
    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Conspiracy Chat Bot — Interactive</title>
        <style>
          * {{ margin: 0; padding: 0; box-sizing: border-box; }}
          body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 2rem;
          }}
          .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
            padding: 2rem;
          }}
          h1 {{
            color: #333;
            margin-bottom: 0.5rem;
            font-size: 2.5rem;
          }}
          .author {{
            color: #666;
            font-size: 0.9rem;
            margin-bottom: 2rem;
            font-style: italic;
          }}
          .form-group {{
            margin-bottom: 1.5rem;
          }}
          label {{
            display: block;
            font-weight: 600;
            color: #333;
            margin-bottom: 0.5rem;
          }}
          textarea {{
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 6px;
            font-size: 1rem;
            font-family: inherit;
            resize: vertical;
            transition: border-color 0.3s;
          }}
          textarea:focus {{
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
          }}
          select {{
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 6px;
            font-size: 1rem;
            cursor: pointer;
            background: white;
            transition: border-color 0.3s;
          }}
          select:focus {{
            outline: none;
            border-color: #667eea;
          }}
          .checkbox-group {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-top: 1rem;
          }}
          input[type="checkbox"] {{
            width: 20px;
            height: 20px;
            cursor: pointer;
          }}
          button {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 32px;
            border: none;
            border-radius: 6px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            margin-top: 1rem;
          }}
          button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.3);
          }}
          button:active {{
            transform: translateY(0);
          }}
          #result {{
            margin-top: 2rem;
            padding-top: 2rem;
            border-top: 2px solid #eee;
          }}
          .result-section {{
            margin-bottom: 2rem;
          }}
          .result-section h3 {{
            color: #667eea;
            margin-bottom: 1rem;
            font-size: 1.2rem;
          }}
          pre {{
            background: #f6f8fa;
            padding: 1rem;
            border-radius: 6px;
            border-left: 4px solid #667eea;
            white-space: pre-wrap;
            word-wrap: break-word;
            overflow-x: auto;
            line-height: 1.6;
            font-size: 0.95rem;
          }}
          .loading {{
            text-align: center;
            padding: 2rem;
            color: #667eea;
            font-weight: 600;
          }}
          .error {{
            background: #fee;
            color: #c33;
            padding: 1rem;
            border-radius: 6px;
            margin-top: 1rem;
            border-left: 4px solid #c33;
          }}
          .success {{
            background: #efe;
            color: #3c3;
            padding: 1rem;
            border-radius: 6px;
            margin-top: 1rem;
            border-left: 4px solid #3c3;
          }}
        </style>
      </head>
      <body>
        <div class="container">
          <h1>🤖 Conspiracy Chat Bot</h1>
          <div class="author">Author: <strong>Jimbo</strong></div>
          
          <div class="form-group">
            <label for="q">Your Question:</label>
            <textarea id="q" name="question" placeholder="Ask me anything...">Explain Newton's second law.</textarea>
          </div>
          
          <div class="form-group">
            <label for="backend">AI Backend:</label>
            <select id="backend" name="backend">
              <option value="openai" selected>🔵 OpenAI (GPT-4o-mini)</option>
              <option value="anthropic">🔴 Anthropic (Claude)</option>
              <option value="llama">🟡 Local LLaMA</option>
            </select>
          </div>
          
          <div class="checkbox-group">
            <input type="checkbox" id="steps" checked />
            <label for="steps" style="margin: 0;">Show internal reasoning steps (initial → critique → final)</label>
          </div>
          
          <button type="button" onclick="submitQuestion()">🚀 Ask</button>
          
          <div id="result"></div>
        </div>
        
        <script>
          async function submitQuestion() {{
            const q = document.getElementById('q').value.trim();
            if (!q) {{
              alert('Please enter a question!');
              return;
            }}
            
            const backend = document.getElementById('backend').value;
            const show_steps = document.getElementById('steps').checked;
            const resDiv = document.getElementById('result');
            
            resDiv.innerHTML = '<div class="loading">⏳ Thinking... (this may take 10-30 seconds)</div>';
            
            try {{
              const resp = await fetch('/think', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ question: q, backend: backend, show_steps: show_steps }})
              }});
              
              if (!resp.ok) {{
                const error = await resp.json();
                resDiv.innerHTML = '<div class="error"><strong>Error:</strong> ' + escapeHtml(error.error || 'Unknown error') + '</div>';
                return;
              }}
              
              const data = await resp.json();
              let html = '<div class="success">✅ Reasoning complete!</div>';
              
              if (show_steps) {{
                html += '<div class="result-section">';
                html += '<h3>1️⃣ Initial Answer</h3>';
                html += '<pre>' + escapeHtml(data.initial || '') + '</pre>';
                html += '</div>';
                
                html += '<div class="result-section">';
                html += '<h3>2️⃣ Critique</h3>';
                html += '<pre>' + escapeHtml(data.critique || '') + '</pre>';
                html += '</div>';
                
                html += '<div class="result-section">';
                html += '<h3>3️⃣ Final Answer</h3>';
                html += '<pre>' + escapeHtml(data.final || '') + '</pre>';
                html += '</div>';
              }} else {{
                html += '<div class="result-section">';
                html += '<h3>Final Answer</h3>';
                html += '<pre>' + escapeHtml(data.final || JSON.stringify(data)) + '</pre>';
                html += '</div>';
              }}
              
              resDiv.innerHTML = html;
            }} catch (err) {{
              resDiv.innerHTML = '<div class="error"><strong>Network Error:</strong> ' + escapeHtml(String(err)) + '</div>';
            }}
          }}
          
          function escapeHtml(str) {{
            if (!str) return '';
            return str
              .replace(/&/g, '&amp;')
              .replace(/</g, '&lt;')
              .replace(/>/g, '&gt;')
              .replace(/"/g, '&quot;')
              .replace(/'/g, '&#039;');
          }}
          
          // Allow Enter in textarea to submit with Ctrl+Enter
          document.getElementById('q').addEventListener('keydown', function(e) {{
            if (e.ctrlKey && e.key === 'Enter') {{
              submitQuestion();
            }}
          }});
        </script>
      </body>
    </html>
    """
    return HTMLResponse(content=html)


@click.group()
def cli():
    """CLI for Conspiracy Chat Bot. Use `serve` to run the web server."""
    pass


@cli.command()
@click.option("--host", default="0.0.0.0", help="Host to bind the server to")
@click.option("--port", default=8000, type=int, help="Port to bind the server to")
def serve(host, port):
    """Start the FastAPI web server."""
    logger.info(f"Starting server on {host}:{port}")
    logger.info(f"Open http://localhost:{port}/ui in your browser")
    uvicorn.run("main:app", host=host, port=port, reload=False)


@cli.command()
@click.argument("question")
@click.option("--backend", default="openai", help="Which backend to use: openai, anthropic, llama")
@click.option("--no-steps", "show_steps", flag_value=False, default=True, help="Hide internal steps (initial, critique, final)")
def think(question, backend, show_steps):
    """Run iterative reasoning from the CLI."""
    print(f"\n🤖 Running iterative reasoning using backend={backend}...\n")
    try:
        res = reasoning.iterative_refine(question, backend=backend, show_steps=show_steps)
        
        if show_steps:
            print("\n" + "="*80)
            print("1️⃣  INITIAL ANSWER")
            print("="*80)
            print(res.get("initial", ""))
            
            print("\n" + "="*80)
            print("2️⃣  CRITIQUE")
            print("="*80)
            print(res.get("critique", ""))
            
            print("\n" + "="*80)
            print("3️⃣  FINAL ANSWER")
            print("="*80)
            print(res.get("final", ""))
        else:
            print(res.get("final", ""))
        
        print("\n" + "="*80 + "\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")
        raise SystemExit(1)


@cli.command()
@click.argument("name", default="Jimbo")
def greet(name):
    """Friendly greeting command."""
    print(f"\n👋 Hello, {name}! Welcome to Conspiracy Chat Bot by Jimbo.\n")


if __name__ == "__main__":
    cli()
