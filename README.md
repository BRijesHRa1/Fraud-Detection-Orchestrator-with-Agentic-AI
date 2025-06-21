# Fraud Detection Orchestrator with Agentic AI

A simple, local fraud detection system using collaborative AI agents built with CrewAI, FastAPI, and Ollama.

## Features

- **Real-time Fraud Detection**: Analyze transactions in under 500ms
- **Collaborative AI Agents**: Multiple specialized agents vote on fraud risk
- **Local LLM Integration**: Uses Ollama for privacy and local processing
- **SQLite Database**: Simple local storage for transactions and analysis
- **REST API**: Clean FastAPI interface for integration


## Architecture Overview:

                        ┌──────────────────────┐
                        │      Client/API      │
                        │    (FastAPI + LLM)   │
                        └─────────┬────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │    Fraud Detection Core   │
                    │       (CrewAI Agents)     │
                    └──────┬──────┬──────┬──────┘
                           │      │      │
                  ┌────────▼──┐ ┌─▼────────┐ ┌─────────▼──┐
                  │  AI Agent │ │ AI Agent │ │  AI Agent  │
                  └────┬──────┘ └────┬─────┘ └──────┬────┘
                       │              │              │
                       │       ┌──────▼──────┐       │
                       └──────▶│   ChromaDB  │◀──────┘
                               └──────┬──────┘
                                      │
                               ┌──────▼──────┐
                               │ Voting Engine│
                               └──────┬──────┘
                                      │
                               ┌──────▼──────┐
                               │ Block/Allow │
                               └─────────────┘
                                      │
                                 ┌────▼────┐
                                 │ SQLite  │
                                 └─────────┘
                                      │
                                ┌─────▼──────┐
                                │   Docker   │
                                └────────────┘


## Project Structure

```
Fraud-Detection-Orchestrator-with-Agentic-AI/
├── app/
│   ├── agents/          # AI agents for fraud detection
│   ├── api/             # FastAPI routes
│   ├── config/          # Configuration settings
│   ├── database/        # SQLite database setup
│   ├── models/          # Pydantic data models
│   └── services/        # Business logic services
├── docker/              # Docker configuration files
│   ├── Dockerfile       # Application container
│   ├── docker-compose.yml # Complete system orchestration
│   └── .dockerignore    # Docker build exclusions
├── main.py              # FastAPI application entry point
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Quick Start

### Option 1: Docker (Recommended) 🐳

The easiest way to run the system is with Docker:

```bash
# Navigate to docker folder and start the entire system
cd docker
docker-compose up -d

# Check if everything is running
docker-compose ps
```

The API will be available at: `http://localhost:8000`

**Note**: The first run will take a few minutes to download the Ollama model (llama2).

### Option 2: Local Setup

#### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 2. Install and Start Ollama

```bash
# Install Ollama (https://ollama.ai)
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a model (e.g., llama2)
ollama pull llama2

# Start Ollama server
ollama serve
```

#### 3. Run the Application

```bash
python main.py
```

The API will be available at: `http://127.0.0.1:8000`

## API Endpoints

- **GET /** - Root endpoint with system info
- **POST /api/v1/fraud/analyze** - Analyze a transaction for fraud
- **POST /api/v1/fraud/quick-test** - Quick test with sample transaction
- **GET /api/v1/fraud/health** - Health check endpoint
- **GET /docs** - Interactive API documentation

## Quick Test

Once the server is running, you can test it:

**For Docker setup:**
```bash
curl -X POST "http://localhost:8000/api/v1/fraud/quick-test"
```

**For local setup:**
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/fraud/quick-test"
```

Or visit the interactive API documentation:
- Docker: `http://localhost:8000/docs`
- Local: `http://127.0.0.1:8000/docs`

**Run the test script:**
```bash
python test_system.py
```

## How It Works

1. **Transaction Analysis**: When a transaction is submitted, it's analyzed by 4 specialized AI agents:

   - **Amount Analysis Agent**: Checks for unusual spending patterns
   - **Behavioral Analysis Agent**: Analyzes user behavior anomalies
   - **Location Analysis Agent**: Evaluates geographic risk factors
   - **Risk Assessment Agent**: Makes final fraud determination
2. **Collaborative Decision**: All agents vote on the transaction, and the system provides:

   - Fraud probability score
   - Risk factors identified
   - Final recommendation (approve/decline/review)
3. **Fast Response**: Designed to process transactions in under 500ms

## Technologies Used

- **Python**: Core programming language
- **FastAPI**: Web framework for APIs
- **CrewAI**: Multi-agent AI framework
- **Ollama**: Local LLM runtime
- **SQLite**: Local database
- **ChromaDB**: Vector database for pattern storage
- **Docker**: Containerization for easy deployment

## Configuration

### Docker Environment Variables

You can customize the system by setting environment variables in the docker-compose.yml:

```yaml
environment:
  - OLLAMA_URL=http://ollama:11434
  - DATABASE_URL=sqlite:///./data/fraud_detection.db
  - CHROMA_DB_PATH=./chroma_db
  - FRAUD_THRESHOLD=0.7
  - OLLAMA_MODEL=llama2
```

### Local Configuration

Edit `app/config/settings.py` to customize:

- Fraud detection threshold
- Ollama model and URL
- Database settings
- API host and port

## Docker Commands

All Docker commands should be run from the `docker/` directory:

```bash
cd docker

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up --build -d

# Clean up (removes volumes)
docker-compose down -v
```
