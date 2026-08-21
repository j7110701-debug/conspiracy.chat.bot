# main.py
# Author: j7110701-debug
# Conspiracy Chat Bot — lightweight FastAPI + CLI app

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import click
import uvicorn
from pydantic import BaseModel
from typing import Optional

import reasoning_iter as reasoning

app = FastAPI(title="Conspiracy Chat Bot", description="Iterative-reasoning assistant (author: j7110701-debug)")

@app.get("/")
def read_root():
    return {"message": "Hello from my Python app!", "author": "j7110701-debug"}

class ThinkRequest(BaseModel):
    question: str
    backend: Optional[str] = "openai"  # openai | anthropic | llama
    show_steps: Optional[bool] = True

@app.post("/think")
def think(req: ThinkRequest):
    """Endpoint to run iterative refinement reasoning using specified backend."""
    result = reasoning.iterative_refine(req.question, backend=req.backend, show_steps=req.show_steps)
    return JSONResponse(content=result)

@app.get("/ui", response_class=HTMLResponse)
async def ui(request: Request):
    """Simple UI to submit a question and view initial/critique/final outputs.
    This page proudly displays the app author throughout.
    """
    html = f"""
    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8" />
        <title>Conspiracy Chat Bot — Interactive</title>
        <style>
          body {{ font-family: Arial, sans-serif; max-width: 900px; margin: 2rem auto; padding: 1rem; }}
          textarea {{ width: 100%; height: 120px; }}
          pre {{ background: #f6f8fa; padding: 1rem; white-space: pre-wrap; }}</style>
      </head>
      <body>
        <h1>Conspiracy Chat Bot</h1>
        <p>Author: <strong>j7110701-debug</strong></p>
        <form id="thinkForm">
          <label for="q">Question:</label><br />
          <textarea id="q" name="question">Explain Newton's second law.</textarea><br />
          <label for="backend">Backend:</label>
          <select id="backend" name="backend">
            <option value="openai" selected>OpenAI</option>
            <option value="anthropic">Anthropic (if configured)</option>
            <option value="llama">Local LLaMA (if configured)</option>
          </select>
          <label><input type="checkbox" id="steps" checked /> Show internal steps</label>
          <br /><br />
          <button type="button" onclick="submitQuestion()">Ask</button>
        </form>
        <h2>Result (Author: j7110701-debug)</h2>
        <div id="result">
          <em>Responses will appear here.</em>
        </div>
        <script>
          async function submitQuestion() {{
            const q = document.getElementById('q').value;
            const backend = document.getElementById('backend').value;
            const show_steps = document.getElementById('steps').checked;
            const resDiv = document.getElementById('result');
            resDiv.innerHTML = '<p>Thinking... (this may take a few seconds)</p>';
            try {{
              const resp = await fetch('/think', {{
                method: 'POST', headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ question: q, backend: backend, show_steps: show_steps }})
              }});
              const data = await resp.json();
              let html = '';
              if (data.initial) html += '<h3>Initial Answer</h3><pre>' + escapeHtml(data.initial) + '</pre>';
              if (data.critique) html += '<h3>Critique</h3><pre>' + escapeHtml(data.critique) + '</pre>';
              html += '<h3>Final Answer</h3><pre>' + escapeHtml(data.final || data['final'] || JSON.stringify(data)) + '</pre>';
              resDiv.innerHTML = html;
            }} catch (err) {{
              resDiv.innerHTML = '<pre>Error: ' + err + '</pre>';
            }}
          }}
          function escapeHtml(str) {{
            if (!str) return '';
            return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
          }}
        </script>
      </body>
    </html>
    """
    return HTMLResponse(content=html)

@click.group()
def cli():
    """CLI for the app. Use `serve` to run the web server or add other commands."""
    pass

@cli.command()
@click.option("--host", default="0.0.0.0", help="Host to bind the server to")
@click.option("--port", default=8000, type=int, help="Port to bind the server to")
def serve(host, port):
    """Start the FastAPI web server."""
    # uvicorn.run accepts "module:app" string; using main:app here
    uvicorn.run("main:app", host=host, port=port)

@cli.command()
@click.argument("name", default="world")
def greet(name):
    """Example CLI task."""
    print(f"Hello, {name}!")

@cli.command()
@click.argument("question")
@click.option("--backend", default="openai", help="Which backend to use: openai, anthropic, llama")
@click.option("--no-steps", "show_steps", default=True, is_flag=True, help="Show internal steps (initial, critique, final)")
def think(question, backend, show_steps):
    """Run iterative reasoning from the CLI and print the results."""
    print(f"Running iterative reasoning using backend={backend}...\n")
    res = reasoning.iterative_refine(question, backend=backend, show_steps=show_steps)
    if show_steps:
        print("=== INITIAL ANSWER ===")
        print(res.get("initial", ""))
        print("\n=== CRITIQUE ===")
        print(res.get("critique", ""))
        print("\n=== FINAL ANSWER ===")
        print(res.get("final", ""))
    else:
        print(res.get("final", ""))

if __name__ == "__main__":
    cli()
