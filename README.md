# First Agent

A lightweight local agent starter built with `smolagents`, `LiteLLMModel`, and a Gradio chat interface. It is configured to run against a local Ollama model instead of a hosted Hugging Face model, which makes it easy to develop and test an agent entirely on your machine.

## What this project contains

- A `CodeAgent` configured with a local Ollama backend
- A streamed Gradio UI that displays tool calls and reasoning steps
- A small custom tool for getting the current time in a timezone
- Prompt templates stored in YAML for agent behavior
- A minimal final-answer tool for structured completion

## Repository layout

- `app.py` — creates the agent and launches the app
- `Gradio_UI.py` — Gradio interface and streaming message handling
- `prompts.yaml` — agent system prompt and planning templates
- `agent.json` — metadata used by Hugging Face Spaces-style publishing
- `requirements.txt` — pinned Python dependencies
- `tools/final_answer.py` — custom final answer tool

## Prerequisites

- Python 3.10+
- Ollama installed and running locally
- A model pulled into Ollama, such as `qwen2:7b`

## Local setup

### 1) Install Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Then start the local service:

```bash
ollama serve
```

### 2) Pull a model

```bash
ollama pull qwen2:7b
```

You can change the model later with the `OLLAMA_MODEL` environment variable.

### 3) Create and activate a Python environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4) Install Python dependencies

```bash
pip install -r requirements.txt
```

### 5) Run the app

The project now supports either Ollama or a free Hugging Face model.

Using the included launcher script:

```bash
./run_app.sh
```

Or run directly:

```bash
python app.py
```

If you use the bundled environment:

```bash
./env/bin/python app.py
```

The Gradio app will print a local URL in the terminal. Open it in your browser to chat with the agent.

## Configuration

The app supports two modes:

- `ollama` for local models
- `huggingface` for free Hugging Face inference models

The defaults are:

```bash
export MODEL_MODE=huggingface
export HF_MODEL=Qwen/Qwen2.5-1.5B-Instruct
export HF_TOKEN=""
export OLLAMA_MODEL=qwen2:7b
export OLLAMA_BASE_URL=http://localhost:11434
```

Use a Hugging Face model:

```bash
export MODEL_MODE=huggingface
export HF_MODEL=Qwen/Qwen2.5-1.5B-Instruct
export HF_TOKEN=your_hf_token_here
./run_app.sh
```

Use Ollama instead:

```bash
export MODEL_MODE=ollama
export OLLAMA_MODEL=qwen2:7b
export OLLAMA_BASE_URL=http://localhost:11434
./run_app.sh
```

Only free/open models should be used by default. The recommended default Hugging Face model is:

```text
Qwen/Qwen2.5-1.5B-Instruct
```

## Verified local run example

This project was successfully run locally with Ollama using the `qwen2:7b` model. A typical terminal run looked like this:

```text
╭─────────────────────────────────────────────────────────────────────────── New run ───────────────────────────────────────────────────────────────────────────╮
│                                                                                                                                                               │
│ Hello                                                                                                                                                         │
│                                                                                                                                                               │
╰─ LiteLLMModel - ollama/qwen2:7b ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Step 1 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 ─ Executing parsed code: ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── 
  final_answer("Hello! How can I assist you today?")                                                                                                             
 ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── 
Out - Final answer: Hello! How can I assist you today?
[Step 1: Duration 130.68 seconds| Input tokens: 2,023 | Output tokens: 43]
```

This confirms the local stack is working end-to-end with:

- Ollama serving a local model
- `LiteLLMModel` proxying requests through `ollama/qwen2:7b`
- `smolagents` executing the task
- a Gradio front end streaming the response

## Current architecture and environment

This project currently runs as a local single-machine architecture:

```text
User browser
    │
    ▼
Gradio UI (local Python app)
    │
    ▼
CodeAgent / smolagents
    │
    ▼
LiteLLMModel -> Ollama local API
    │
    ▼
Local model runtime (qwen2:7b)
```

### Environment notes

- Operating system: Linux (Ubuntu 22.04.1 LTS based on AWS kernel 6.8.0-1066-aws)
- CPU: Intel Xeon Platinum 8488C, 2 physical cores / 4 logical threads, x86_64
- Memory: 15 GiB RAM, with ~5.2 GiB available at runtime
- Swap: 30 GiB
- Local inference backend: Ollama
- Model: `qwen2:7b`
- App layer: Python + Gradio + `smolagents`
- Server pattern: local desktop/server-side execution, not remote cloud inference

This is useful context for future debugging, reproducibility, and migration planning.

## Customization points

You can extend the project by:

- adding more tools in `app.py`
- updating the system prompt in `prompts.yaml`
- changing the Gradio interface or log formatting in `Gradio_UI.py`
- swapping the Ollama model for another locally available one

## Troubleshooting

### Model is not supported

If you see an error like:

```text
The requested model 'Qwen/Qwen2.5-Coder-32B-Instruct' is not supported by any provider you have enabled.
```

that usually means the app is trying to use a hosted Hugging Face model ID instead of a local Ollama model.

Use a local Ollama model name such as:

```bash
OLLAMA_MODEL=qwen2:7b
```

and ensure Ollama is running:

```bash
ollama serve
ollama list
```

### Token-count errors in Gradio

This repo includes a safe guard against missing token metadata from local models. If your Ollama model does not report token counts, the app should still run without crashing.

## Notes

This template is designed for local experimentation and rapid agent prototyping. It is intentionally simple and easy to extend, but it is not a production deployment setup out of the box.

For a production-quality service, you would typically add:

- environment-based secrets management
- logging and monitoring
- authentication
- persistent storage
- a proper deployment layer
