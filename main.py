from fastapi import FastAPI
import click
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from my Python app!"}

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

if __name__ == "__main__":
    cli()
