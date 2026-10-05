# Intsall ollama
curl -fsSL https://ollama.com/install.sh | sh

# Create environment
python3 -m venv .venv
source .venv/bin/activate

# Install PIP 
python -m pip install --upgrade pip
pip install "fastapi[standard]" ollama pytest

ollama pull qwen3:4b


# Start API Server
python -m uvicorn app.main:app --reload

# Swagger URL
curl http://127.0.0.1:8000/

# Health URL
curl http://127.0.0.1:8000/health

# AI agent end point
curl -X POST \
  http://127.0.0.1:8000/agent/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Show me all pending tasks"}'


# To run python test
python -m pytest -v

  

