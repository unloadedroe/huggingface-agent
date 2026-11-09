import yaml
from smolagents import CodeAgent, LiteLLMModel, load_tool, tool
from tools.final_answer import FinalAnswerTool

from Gradio_UI import GradioUI
from config import get_current_time_in_timezone, get_model_config

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