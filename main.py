from fastapi import FastAPI
import click
import uvicorn
from pydantic import BaseModel
from typing import Optional

import reasoning_iter as reasoning

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from my Python app!"}

class ThinkRequest(BaseModel):
    question: str
    backend: Optional[str] = "openai"  # openai | anthropic | llama
    show_steps: Optional[bool] = True

@app.post("/think")
def think(req: ThinkRequest):
    """Endpoint to run iterative refinement reasoning using specified backend."""
    result = reasoning.iterative_refine(req.question, backend=req.backend, show_steps=req.show_steps)
    return result

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
