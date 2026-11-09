import os
import datetime
import requests
import pytz
import yaml
from smolagents import CodeAgent, LiteLLMModel, load_tool, tool
from tools.final_answer import FinalAnswerTool

from Gradio_UI import GradioUI

# Below is an example of a tool that does nothing. Amaze us with your creativity !
@tool
def my_custom_tool(arg1:str, arg2:int)-> str: #it's import to specify the return type
    #Keep this format for the description / args / args description but feel free to modify the tool
    """A tool that does nothing yet 
    Args:
        arg1: the first argument
        arg2: the second argument
    """
    return "What magic will you build ?"

@tool
def get_current_time_in_timezone(timezone: str) -> str:
    """A tool that fetches the current local time in a specified timezone.
    Args:
        timezone: A string representing a valid timezone (e.g., 'America/New_York').
    """
    try:
        # Create timezone object
        tz = pytz.timezone(timezone)
        # Get current time in that timezone
        local_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return f"The current local time in {timezone} is: {local_time}"
    except Exception as e:
        return f"Error fetching time for timezone '{timezone}': {str(e)}"


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


final_answer = FinalAnswerTool()
model_config = get_model_config()
model = LiteLLMModel(
    model_id=model_config["model_id"],
    api_base=model_config["api_base"],
    api_key=model_config["api_key"],
    max_tokens=model_config["max_tokens"],
    temperature=model_config["temperature"],
    custom_role_conversions=None,
)


# Import tool from Hub
image_generation_tool = load_tool("agents-course/text-to-image", trust_remote_code=True)

with open("prompts.yaml", 'r') as stream:
    prompt_templates = yaml.safe_load(stream)
    
agent = CodeAgent(
    model=model,
    tools=[final_answer], ## add your tools here (don't remove final answer)
    max_steps=6,
    verbosity_level=1,
    grammar=None,
    planning_interval=None,
    name=None,
    description=None,
    prompt_templates=prompt_templates
)


if __name__ == "__main__":
    GradioUI(agent).launch()