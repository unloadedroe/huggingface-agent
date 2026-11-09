import os
import datetime

import pytz

FREE_HF_MODELS = {
    "ollama": "qwen2:7b",
    "huggingface": "Qwen/Qwen2.5-1.5B-Instruct",
}

DEFAULT_MODE = os.getenv("MODEL_MODE", "ollama").lower()
DEFAULT_HF_MODEL = os.getenv("HF_MODEL", FREE_HF_MODELS["huggingface"])
DEFAULT_OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", FREE_HF_MODELS["ollama"])
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
HF_TOKEN = os.getenv("HF_TOKEN", "")


def get_model_config():
    mode = os.getenv("MODEL_MODE", DEFAULT_MODE).lower()
    if mode not in {"ollama", "huggingface"}:
        mode = "ollama"

    if mode == "huggingface":
        model_name = os.getenv("HF_MODEL", DEFAULT_HF_MODEL).strip()
        if model_name.startswith("huggingface/"):
            model_name = model_name.replace("huggingface/", "", 1)
        if model_name.startswith("http://") or model_name.startswith("https://"):
            full_model_id = model_name
        else:
            full_model_id = f"huggingface/{model_name}"

        return {
            "provider": "huggingface",
            "model_id": full_model_id,
            "api_base": None,
            "api_key": HF_TOKEN,
            "max_tokens": 2048,
            "temperature": 0.5,
        }

    model_name = os.getenv("OLLAMA_MODEL", DEFAULT_OLLAMA_MODEL)
    return {
        "provider": "ollama",
        "model_id": f"ollama/{model_name}",
        "api_base": OLLAMA_BASE_URL,
        "api_key": "ollama",
        "max_tokens": 2048,
        "temperature": 0.5,
    }


def get_current_time_in_timezone(timezone: str) -> str:
    """Fetch the current local time in a specified timezone."""
    try:
        tz = pytz.timezone(timezone)
        local_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return f"The current local time in {timezone} is: {local_time}"
    except Exception as exc:
        return f"Error fetching time for timezone '{timezone}': {str(exc)}"
