# Crypto Market Monitoring & Automation Dashboard

A production-ready Crypto Market Monitoring & Automation Dashboard built for a fintech/crypto analytics environment.

## 🚀 Features

- **Data Collection:** Automated API fetch jobs from CoinGecko & Binance with retry mechanisms (Tenacity).
- **RAG AI Copilot:** Advanced LangChain-based AI Agent that queries PostgreSQL (SQL Agent) and ChromaDB to answer complex user queries.
- **ETL Pipelines:** Robust Python Pandas scripts for extracting, cleaning, and loading crypto data into PostgreSQL.
- **Advanced Analytics:** ML price predictions (Scikit-Learn) and volatility-based risk scoring.
- **Automation:** APScheduler-driven alerts, ETL triggers, and AI Insight generation.
- **UI:** Interactive Streamlit dashboard and Conversational AI UI.
- **Backend:** FastAPI for highly concurrent REST endpoints.
- **Deployment:** Fully Dockerized.

## 🛠 Tech Stack
- **Python:** FastAPI, Pandas, LangChain, SQLAlchemy, Scikit-Learn.
- **Database:** PostgreSQL, ChromaDB (Vector Store).
- **Frontend:** Streamlit.
- **Infrastructure:** Docker, Docker Compose.

## 📦 Setup & Run

1. Clone the repository and navigate into it.
2. Copy the environment variables:
   ```bash
   cp .env.example .env
   ```
3. Add your `OPENAI_API_KEY` to the `.env` file for the RAG Copilot to function.
4. Run the containers:
   ```bash
   docker-compose up --build -d
   ```
5. Access the services:
   - FastAPI Backend: `http://localhost:8000/docs`
   - Streamlit UI: `http://localhost:8501`
   - Superset: `http://localhost:8088`

## 📁 Architecture
- `api/` - FastAPI routes and API clients (CoinGecko/Binance).
- `analytics/` - ML Predictors, Risk Scoring, and RAG Agent.
- `automation/` - Schedulers and Alerts.
- `dashboards/` - Streamlit UI and Chat UI.
- `database/` - SQLAlchemy models and DB connection.
- `deployment/` - Dockerfile.
- `etl/` - Pandas ETL jobs.
- `reports/` - AI-generated insights.
