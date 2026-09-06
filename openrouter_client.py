import os
import json
import urllib.request
import urllib.error
from typing import List, Dict, Generator, Tuple, Optional

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODELS_URL = "https://openrouter.ai/api/v1/models"
# Safe key loader
def get_api_key() -> str:
    """Retrieve API key from Streamlit secrets, local file or environment."""
    try:
        import streamlit as st
        if "OPENROUTER_API_KEY" in st.secrets:
            return st.secrets["OPENROUTER_API_KEY"]
    except Exception:
        pass

    if "OPENROUTER_API_KEY" in os.environ:
        return os.environ["OPENROUTER_API_KEY"]

    # Check local secrets.toml directly
    try:
        sec_path = os.path.join(os.path.dirname(__file__), ".streamlit", "secrets.toml")
        if os.path.exists(sec_path):
            with open(sec_path, "r", encoding="utf-8") as f:
                for line in f:
                    if "OPENROUTER_API_KEY" in line and "=" in line:
                        val = line.split("=", 1)[1].strip().strip('"').strip("'")
                        if val:
                            return val
    except Exception:
        pass

    return ""


# Fallback models list in case network fails
FALLBACK_FREE_MODELS = [
    {
        "id": "nvidia/nemotron-3-ultra-550b-a55b:free",
        "name": "NVIDIA: Nemotron 3 Ultra (free)",
        "context_length": 1000000,
        "provider": "NVIDIA",
        "description": "550B MoE (55B active) frontier-reasoning model from NVIDIA with 1M context window."
    },
    {
        "id": "nvidia/nemotron-3.5-lightning:free",
        "name": "NVIDIA: Nemotron 3.5 Lightning (free)",
        "context_length": 1000000,
        "provider": "NVIDIA",
        "description": "30B MoE (3B active) high-speed agentic reasoning model."
    },
    {
        "id": "nvidia/nemotron-3-super-120b-a12b:free",
        "name": "NVIDIA: Nemotron 3 Super (free)",
        "context_length": 262144,
        "provider": "NVIDIA",
        "description": "120B hybrid MoE model (12B active) for complex agentic workflows."
    },
    {
        "id": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
        "name": "NVIDIA: Nemotron 3 Nano Omni (free)",
        "context_length": 256000,
        "provider": "NVIDIA",
        "description": "30B-A3B fast multimodal & reasoning model."
    },
    {
        "id": "google/gemma-4-31b-it:free",
        "name": "Google: Gemma 4 31B (free)",
        "context_length": 262144,
        "provider": "Google",
        "description": "Google DeepMind 30.7B dense instruction & reasoning model."
    },
    {
        "id": "google/gemma-4-26b-a4b-it:free",
        "name": "Google: Gemma 4 26B A4B (free)",
        "context_length": 262144,
        "provider": "Google",
        "description": "DeepMind MoE delivering near-31B quality at high speed."
    },
    {
        "id": "minimax/minimax-m3:free",
        "name": "MiniMax: MiniMax M3 (free)",
        "context_length": 1048576,
        "provider": "MiniMax",
        "description": "1M token context multimodal foundation model."
    },
    {
        "id": "minimax/minimax-m2.7:free",
        "name": "MiniMax: MiniMax M2.7 (free)",
        "context_length": 196608,
        "provider": "MiniMax",
        "description": "Next-gen agentic language model for complex tasks."
    },
    {
        "id": "poolside/laguna-s-2.1:free",
        "name": "Poolside: Laguna S 2.1 (free)",
        "context_length": 262144,
        "provider": "Poolside",
        "description": "118B (8B active) advanced coding agent model."
    },
    {
        "id": "poolside/laguna-xs-2.1:free",
        "name": "Poolside: Laguna XS 2.1 (free)",
        "context_length": 262144,
        "provider": "Poolside",
        "description": "33B-A3B high-speed coding agent model."
    },
    {
        "id": "cohere/north-mini-code:free",
        "name": "Cohere: North Mini Code (free)",
        "context_length": 256000,
        "provider": "Cohere",
        "description": "30B sparse MoE coding and reasoning model."
    },
    {
        "id": "thinkingmachines/inkling:free",
        "name": "Thinking Machines: Inkling (free)",
        "context_length": 1048576,
        "provider": "Thinking Machines",
        "description": "975B MoE (41B active) multimodal frontier reasoning model."
    },
    {
        "id": "thinkingmachines/inkling-small:free",
        "name": "Thinking Machines: Inkling Small (free)",
        "context_length": 1048576,
        "provider": "Thinking Machines",
        "description": "276B MoE (12B active) efficient multimodal model."
    },
    {
        "id": "liquid/lfm-2.5-2.6b:free",
        "name": "LiquidAI: LFM2.5-2.6B (free)",
        "context_length": 65536,
        "provider": "LiquidAI",
        "description": "Compact reasoning model for RAG and data extraction."
    },
    {
        "id": "dots-studio/dots-3-note-preview:free",
        "name": "Dots Studio: Dots3-Note Preview (free)",
        "context_length": 512000,
        "provider": "Dots Studio",
        "description": "280B MoE (16B active) open-weight reasoning model."
    },
    {
        "id": "inclusionai/ling-3.0-flash-sante:free",
        "name": "InclusionAI: Ling 3.0 Flash Sante (free)",
        "context_length": 262144,
        "provider": "InclusionAI",
        "description": "Medicine and health-focused MoE model."
    },
    {
        "id": "inclusionai/ling-3.0-flash-fin:free",
        "name": "InclusionAI: Ling 3.0 Flash Fin (free)",
        "context_length": 262144,
        "provider": "InclusionAI",
        "description": "Finance and investment-focused MoE model."
    },
    {
        "id": "openrouter/free",
        "name": "OpenRouter: Auto Free Router",
        "context_length": 200000,
        "provider": "OpenRouter",
        "description": "Smart router that automatically routes to the best available free model."
    }
]


def get_api_key() -> str:
    """Retrieve API key from Streamlit secrets, environment or default."""
    try:
        import streamlit as st
        if "OPENROUTER_API_KEY" in st.secrets:
            return st.secrets["OPENROUTER_API_KEY"]
    except Exception:
        pass
    return os.environ.get("OPENROUTER_API_KEY", DEFAULT_API_KEY)


def fetch_free_models(api_key: Optional[str] = None) -> List[Dict]:
    """
    Fetch all free models directly from OpenRouter API.
    Returns a sorted list where NVIDIA and top models come first.
    """
    key = api_key or get_api_key()
    headers = {
        "Authorization": f"Bearer {key}",
        "HTTP-Referer": "http://localhost:8501",
        "X-Title": "Dark Streamlit AI Chat",
        "User-Agent": "StreamlitDarkAIChat/1.0"
    }

    try:
        req = urllib.request.Request(OPENROUTER_MODELS_URL, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as response:
            data = json.loads(response.read().decode("utf-8"))
            raw_models = data.get("data", [])

            free_list = []
            for m in raw_models:
                m_id = m.get("id", "")
                name = m.get("name", m_id)
                pricing = m.get("pricing", {})
                p_prompt = str(pricing.get("prompt", ""))
                p_compl = str(pricing.get("completion", ""))

                # Exclude audio-only / lyria models that are pay-per-clip or non-chat
                if "lyria" in m_id.lower():
                    continue

                is_free = m_id.endswith(":free") or (p_prompt == "0" and p_compl == "0")
                if is_free:
                    provider = m_id.split("/")[0].capitalize() if "/" in m_id else "General"
                    ctx = m.get("context_length", 0)
                    free_list.append({
                        "id": m_id,
                        "name": name,
                        "context_length": ctx,
                        "provider": provider,
                        "description": m.get("description", "Бесплатная нейросеть OpenRouter.")
                    })

            if free_list:
                # Priority sorting: NVIDIA Nemotron 3 Ultra first, then other NVIDIA, then Google, then others
                def sort_priority(item):
                    m_id = item["id"].lower()
                    if "nemotron-3-ultra" in m_id:
                        return 0
                    if "nvidia" in m_id:
                        return 1
                    if "gemma" in m_id:
                        return 2
                    if "minimax" in m_id:
                        return 3
                    return 10

                free_list.sort(key=sort_priority)
                return free_list

    except Exception as e:
        print(f"Notice: Failed to fetch live models ({e}), using rich fallback list.")

    return FALLBACK_FREE_MODELS


def stream_chat_completion(
    model: str,
    messages: List[Dict[str, str]],
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    api_key: Optional[str] = None
) -> Generator[Tuple[str, str], None, None]:
    """
    Streams chat completion from OpenRouter API using SSE.
    Yields tuples of (chunk_type, text):
      - ('reasoning', text) : Reasoning tokens / CoT (if supported by model)
      - ('content', text)   : Normal message content
      - ('error', text)     : Error message if something fails
    """
    key = api_key or get_api_key()

    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "stream": True
    }
    if max_tokens and max_tokens > 0:
        payload["max_tokens"] = max_tokens

    data_bytes = json.dumps(payload).encode("utf-8")

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8501",
        "X-Title": "Dark Streamlit AI Chat",
        "User-Agent": "StreamlitDarkAIChat/1.0"
    }

    req = urllib.request.Request(OPENROUTER_API_URL, headers=headers, data=data_bytes)

    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            for raw_line in resp:
                line = raw_line.decode("utf-8").strip()
                if not line or not line.startswith("data: "):
                    continue

                event_data = line[6:].strip()
                if event_data == "[DONE]":
                    break

                try:
                    chunk = json.loads(event_data)
                    choices = chunk.get("choices", [])
                    if not choices:
                        continue

                    delta = choices[0].get("delta", {})

                    # Check for reasoning / thought chunks
                    reasoning = delta.get("reasoning")
                    if reasoning:
                        yield ("reasoning", reasoning)

                    # Check for normal content chunk
                    content = delta.get("content")
                    if content:
                        yield ("content", content)

                except json.JSONDecodeError:
                    continue

    except urllib.error.HTTPError as e:
        error_body = ""
        try:
            error_body = e.read().decode("utf-8")
            err_json = json.loads(error_body)
            err_msg = err_json.get("error", {}).get("message", error_body)
        except Exception:
            err_msg = error_body or str(e)
        yield ("error", f"Ошибка OpenRouter API ({e.code}): {err_msg}")
    except Exception as e:
        yield ("error", f"Ошибка подключения к сети: {str(e)}")
