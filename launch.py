#!/usr/bin/env python3
"""
Launcher Script for Conspiracy Chat Bot Suite
Author: Jimbo
Choose which app to run: Conspiracy Chat Bot or Digital Clock
"""

import click
import subprocess
import sys


@click.group()
def cli():
    """Conspiracy Chat Bot Suite - Launch your app of choice"""
    pass


@cli.command()
@click.option("--host", default="0.0.0.0", help="Host to bind the server to")
@click.option("--port", default=8000, type=int, help="Port to bind the server to")
def chatbot(host, port):
    """Launch the Conspiracy Chat Bot with FastAPI UI"""
    click.echo(f"\n🤖 Starting Conspiracy Chat Bot...")
    click.echo(f"📍 Server: http://localhost:{port}/ui\n")
    subprocess.run(
        [sys.executable, "-m", "uvicorn", "main:app", "--host", host, "--port", str(port), "--reload"],
        cwd="."
    )


@cli.command()
@click.option("--host", default="0.0.0.0", help="Host to bind the server to")
@click.option("--port", default=8001, type=int, help="Port to bind the server to")
def clock(host, port):
    """Launch the Digital Clock with Time Zones"""
    click.echo(f"\n⏰ Starting Digital Clock...")
    click.echo(f"📍 Server: http://localhost:{port}/ui\n")
    subprocess.run(
        [sys.executable, "-m", "uvicorn", "clock:app", "--host", host, "--port", str(port), "--reload"],
        cwd="."
    )


@cli.command()
def streamlit_chat():
    """Launch the Conspiracy Chat Bot with Streamlit UI"""
    click.echo(f"\n🎨 Starting Streamlit Conspiracy Chat Bot...\n")
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", "streamlit_app.py"],
        cwd="."
    )


@cli.command()
def menu():
    """Interactive menu to choose which app to run"""
    click.clear()
    click.echo("\n" + "="*50)
    click.echo("  🚀 Conspiracy Chat Bot Suite".center(50))
    click.echo("="*50 + "\n")
    
    options = [
        ("1", "🤖 Conspiracy Chat Bot (FastAPI)", "chatbot"),
        ("2", "⏰ Digital Clock (Multiple Time Zones)", "clock"),
        ("3", "🎨 Conspiracy Chat Bot (Streamlit)", "streamlit_chat"),
        ("4", "Exit", None),
    ]
    
    for num, desc, _ in options:
        click.echo(f"  {num}. {desc}")
    
    click.echo("\n" + "="*50 + "\n")
    
    choice = click.prompt("Select an option (1-4)", type=click.Choice(["1", "2", "3", "4"]))
    
    for num, _, cmd in options:
        if num == choice:
            if cmd:
                click.echo(f"\n🚀 Launching option {choice}...\n")
                ctx = click.Context(cli)
                ctx.invoke(globals()[cmd])
            break


@cli.command()
def list_apps():
    """List all available apps"""
    click.echo("\n📱 Available Apps:")
    click.echo("  1. Conspiracy Chat Bot (FastAPI)")
    click.echo("     - Web UI with iterative reasoning")
    click.echo("     - Backend: OpenAI, Anthropic, LLaMA")
    click.echo("     - Port: 8000")
    click.echo("     - Command: python launch.py chatbot")
    click.echo("")
    click.echo("  2. Digital Clock (Time Zones)")
    click.echo("     - Real-time clock across 15 cities")
    click.echo("     - 24h and 12h format toggle")
    click.echo("     - Port: 8001")
    click.echo("     - Command: python launch.py clock")
    click.echo("")
    click.echo("  3. Conspiracy Chat Bot (Streamlit)")
    click.echo("     - Streamlit UI for the chat bot")
    click.echo("     - Beautiful interface with sidebar")
    click.echo("     - Command: python launch.py streamlit_chat")
    click.echo("\n")


if __name__ == "__main__":
    cli()
