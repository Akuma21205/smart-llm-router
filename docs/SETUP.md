# Setup

## Prerequisites

- Python 3.11+
- pip
- OpenRouter API key
- Jev / TypeSafe API credentials
- Git

## 1. Create the project

```bash
mkdir smart-llm-router
cd smart-llm-router

python -m venv .venv
```

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

### macOS/Linux

```bash
source .venv/bin/activate
```

## 2. Install dependencies

```bash
pip install langchain langchain-openai langchain-core fastapi uvicorn python-dotenv pydantic typesafe-sdk
```

Save the environment:

```bash
pip freeze > requirements.txt
```

## 3. Environment variables

Create `.env`:

```env
OPENROUTER_API_KEY=your_openrouter_key
TYPESAFE_API_KEY=your_typesafe_key
```

Never commit `.env`.

Create `.gitignore`:

```gitignore
.venv/
__pycache__/
*.pyc
.env
.pytest_cache/
```

## 4. Provider responsibilities

### Jev

Use the TypeSafe Python SDK for the semantic routing decision.

The first milestone should independently verify:

```text
query
  -> Jev
  -> typed classification
```

### LangChain

Use LangChain for model abstraction and orchestration.

### OpenRouter

Use OpenRouter as the inference/model-access layer. Because OpenRouter exposes an OpenAI-compatible interface, it can be connected through LangChain's OpenAI-compatible integration by configuring the appropriate base URL and API key.

## 5. First milestone

Before building the complete API, verify two independent calls:

### Jev

```text
query
  -> Jev
  -> category + complexity
```

### OpenRouter

```text
query
  -> LangChain
  -> selected OpenRouter model
  -> response
```

Only after both work independently should they be connected.

## 6. Recommended development order

```text
1. Python environment
2. Jev smoke test
3. OpenRouter smoke test
4. Typed routing result
5. Deterministic routing policy
6. LangChain integration
7. Combined pipeline
8. FastAPI endpoint
9. Telemetry
10. Evaluation
```

## 7. Security

Do not expose either API key to a browser.

All provider calls should happen server-side.

Do not log:

- API keys
- authorization headers
- full sensitive user prompts in production telemetry

For development, store only the minimum data needed for debugging.
