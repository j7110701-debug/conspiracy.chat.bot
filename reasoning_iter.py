# reasoning_iter.py
# Iterative refinement: initial answer -> critique -> revised final answer.
# Supports OpenAI out of the box. Anthropic and local Llama are stubbed with instructions.

import os
from typing import Dict

# Optional: import OpenAI client if installed
try:
    import openai
except Exception:
    openai = None

SYSTEM_PROMPT = "You are a helpful assistant that answers thoroughly and explains reasoning steps."


def _call_openai(messages, model="gpt-4o-mini", max_tokens=800):
    if openai is None:
        raise RuntimeError("openai package not installed. Run: pip install openai")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable not set.")
    openai.api_key = api_key
    resp = openai.ChatCompletion.create(model=model, messages=messages, max_tokens=max_tokens)
    return resp.choices[0].message["content"]


def _call_anthropic(messages_or_prompt: str):
    # Stub: to enable Anthropic, install & use their client:
    # pip install anthropic
    # Then implement a call using the Anthropic API (HUMAN_PROMPT / AI_PROMPT wrappers)
    raise NotImplementedError(
        "Anthropic client not implemented here. To enable: pip install anthropic and implement _call_anthropic using the Anthropic Python API."
    )


def _call_local_llama(messages_or_prompt: str):
    # Stub: to run a local LLaMA-style model, you can use:
    # - llama-cpp-python (fast, uses ggml binaries)
    #   pip install llama-cpp-python
    #   from llama_cpp import Llama
    #   llm = Llama(model_path='/path/to/ggml-model.bin')
    #   out = llm(messages_or_prompt, max_tokens=512)
    # - transformers + local weights (requires torch + a model)
    raise NotImplementedError(
        "Local Llama not implemented here. To enable: install llama-cpp-python or transformers and implement _call_local_llama."
    )


def _backend_call(messages_or_prompt, backend="openai", **kwargs):
    if backend == "openai":
        return _call_openai(messages_or_prompt, **kwargs)
    if backend == "anthropic":
        return _call_anthropic(messages_or_prompt)
    if backend in ("llama", "local-llama"):
        return _call_local_llama(messages_or_prompt)
    raise ValueError(f"Unknown backend: {backend}")


def iterative_refine(question: str, backend: str = "openai", show_steps: bool = True) -> Dict[str, str]:
    """
    Run iterative refinement: initial answer, critique, revised answer.
    Returns dict with keys: initial, critique, final (strings).
    """
    # 1) Initial answer request (ask for step-by-step reasoning)
    init_messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Answer this question and show step-by-step reasoning:\n\n{question}\n\nBe explicit about each step."}
    ]
    try:
        initial = _backend_call(init_messages, backend=backend)
    except Exception as e:
        raise RuntimeError(f"Error calling backend for initial answer: {e}")

    # 2) Critique step: ask model to critique the initial answer
    critique_messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": initial},
        {"role": "user", "content": "Please critique the above answer: find mistakes, missing steps, or weak assumptions (be explicit)."}
    ]
    try:
        critique = _backend_call(critique_messages, backend=backend)
    except Exception as e:
        raise RuntimeError(f"Error calling backend for critique: {e}")

    # 3) Revision step: produce a corrected final answer that addresses the critique
    revise_messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": f"Initial answer:\n{initial}\n\nCritique:\n{critique}"},
        {"role": "user", "content": "Now produce a corrected, concise final answer that addresses the critique and show the minimal step-by-step reasoning."}
    ]
    try:
        final = _backend_call(revise_messages, backend=backend)
    except Exception as e:
        raise RuntimeError(f"Error calling backend for final answer: {e}")

    if show_steps:
        return {"initial": initial, "critique": critique, "final": final}
    else:
        return {"final": final}
