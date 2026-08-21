# reasoning_iter.py
# Iterative refinement: initial answer -> critique -> revised final answer.
# Supports OpenAI, Anthropic, and local Llama.

import os
from typing import Dict
import logging

logger = logging.getLogger(__name__)

# Optional: import clients
try:
    from openai import OpenAI
    HAS_OPENAI = True
except Exception:
    HAS_OPENAI = False

try:
    import anthropic
    HAS_ANTHROPIC = True
except Exception:
    HAS_ANTHROPIC = False

try:
    from llama_cpp import Llama
    HAS_LLAMA = True
except Exception:
    HAS_LLAMA = False

SYSTEM_PROMPT = "You are a helpful assistant that answers thoroughly and explains reasoning steps."


def _call_openai(messages, model="gpt-4o-mini", max_tokens=800):
    """Call OpenAI API with messages."""
    if not HAS_OPENAI:
        raise RuntimeError("openai package not installed. Run: pip install openai")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable not set. Create .env file.")
    
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content


def _call_anthropic(messages, model=None):
    """Call Anthropic API with messages."""
    if not HAS_ANTHROPIC:
        raise RuntimeError(
            "anthropic package not installed. Run: pip install anthropic"
        )
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY environment variable not set. Create .env file.")
    
    if model is None:
        model = os.getenv("ANTHROPIC_MODEL", "claude-3-opus-20240229")
    
    client = anthropic.Anthropic(api_key=api_key)
    
    # Convert to Anthropic format (they use different role names)
    response = client.messages.create(
        model=model,
        max_tokens=1024,
        messages=messages
    )
    return response.content[0].text


def _call_local_llama(messages_or_prompt: str):
    """Call local LLaMA model."""
    if not HAS_LLAMA:
        raise RuntimeError(
            "llama-cpp-python package not installed. Run: pip install llama-cpp-python"
        )
    
    model_path = os.getenv("LLAMA_MODEL_PATH")
    if not model_path or not os.path.exists(model_path):
        raise RuntimeError(
            f"LLAMA_MODEL_PATH not set or model file not found at {model_path}"
        )
    
    llm = Llama(model_path=model_path, n_gpu_layers=-1)
    
    # Handle both message format and plain prompt
    if isinstance(messages_or_prompt, list):
        # Reconstruct prompt from messages
        prompt_text = ""
        for msg in messages_or_prompt:
            prompt_text += f"{msg.get('role', 'user').upper()}: {msg.get('content', '')}\n"
    else:
        prompt_text = messages_or_prompt
    
    output = llm(prompt_text, max_tokens=512, temperature=0.7)
    return output["choices"][0]["text"]


def _backend_call(messages, backend="openai", **kwargs):
    """Route to appropriate backend."""
    if backend == "openai":
        return _call_openai(messages, **kwargs)
    elif backend == "anthropic":
        return _call_anthropic(messages, **kwargs)
    elif backend in ("llama", "local-llama"):
        return _call_local_llama(messages)
    else:
        raise ValueError(f"Unknown backend: {backend}")


def iterative_refine(question: str, backend: str = "openai", show_steps: bool = True) -> Dict[str, str]:
    """
    Run iterative refinement: initial answer -> critique -> revised answer.
    Returns dict with keys: initial, critique, final (strings).
    """
    logger.info(f"Starting iterative refinement with backend={backend}")
    
    # 1) Initial answer request
    init_messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Answer this question and show step-by-step reasoning:\n\n{question}\n\nBe explicit about each step."}
    ]
    try:
        initial = _backend_call(init_messages, backend=backend)
        logger.info("Initial answer generated successfully")
    except Exception as e:
        error_msg = f"Error calling {backend} for initial answer: {e}"
        logger.error(error_msg)
        raise RuntimeError(error_msg)

    # 2) Critique step
    critique_messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": initial},
        {"role": "user", "content": "Please critique the above answer: find mistakes, missing steps, or weak assumptions (be explicit)."}
    ]
    try:
        critique = _backend_call(critique_messages, backend=backend)
        logger.info("Critique generated successfully")
    except Exception as e:
        error_msg = f"Error calling {backend} for critique: {e}"
        logger.error(error_msg)
        raise RuntimeError(error_msg)

    # 3) Revision step
    revise_messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": f"Initial answer:\n{initial}\n\nCritique:\n{critique}"},
        {"role": "user", "content": "Now produce a corrected, concise final answer that addresses the critique and show the minimal step-by-step reasoning."}
    ]
    try:
        final = _backend_call(revise_messages, backend=backend)
        logger.info("Final answer generated successfully")
    except Exception as e:
        error_msg = f"Error calling {backend} for final answer: {e}"
        logger.error(error_msg)
        raise RuntimeError(error_msg)

    if show_steps:
        return {"initial": initial, "critique": critique, "final": final}
    else:
        return {"final": final}
