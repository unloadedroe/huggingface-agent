import yaml
from smolagents import CodeAgent, LiteLLMModel, load_tool
from tools.agent_tools import get_current_time_in_timezone, my_custom_tool
from tools.final_answer import FinalAnswerTool

from Gradio_UI import GradioUI
from config import get_model_config

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
    tools=[my_custom_tool, get_current_time_in_timezone, final_answer],
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