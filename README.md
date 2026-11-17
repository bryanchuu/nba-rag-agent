# NBA RAG Agent

An AI-powered NBA chatbot that combines SQL querying with vector search to answer both statistical and biographical questions about NBA players. Built using LangChain, LangGraph, and OpenAI.

## Features

- **SQL Agent** — Query 40 seasons (1984-2025) of NBA player statistics stored in SQLite
- **Vector Search (RAG)** — Search biographical information for the top 500 all-time scorers using ChromaDB
- **Smart Routing** — The LLM automatically routes questions to the right tool based on the query type
- **Conversation Memory** — Maintains chat history within a session for follow-up questions
- **Streamlit UI** — Web-based chat interface for easy interaction

## Tech Stack

| Component | Technology |
|-----------|------------|
| LLM | OpenAI GPT-4o-mini |
| Agent Framework | LangGraph (ReAct pattern) |
| SQL Database | SQLite |
| Vector Store | ChromaDB |
| Embeddings | OpenAI Embeddings |
| Web UI | Streamlit |
| Data Source | NBA API, Wikipedia |

## Project Structure

```
nba-rag-agent/
├── setup_db.py          # Pulls 40 seasons of stats from NBA API, builds SQLite DB
├── scrape_bios.py       # Scrapes Wikipedia bios for top 500 all-time scorers
├── build_vectorstore.py # Chunks bios and builds ChromaDB vector store
├── agent.py             # Phase 1: SQL-only agent (standalone)
├── rag_agent.py         # Phase 2: Combined SQL + RAG agent (main agent)
├── app.py               # Streamlit web UI
├── test_nba.py          # Quick test for NBA API connectivity
├── test_db.py           # SQL verification queries
├── nba_stats.db         # SQLite database (generated)
├── nba_bios_vectordb/   # ChromaDB vector store (generated)
└── player_bios/         # Raw Wikipedia bio text files (generated)
```

## How It Works

1. **Data Pipeline**: `setup_db.py` pulls player stats from the NBA API and stores them in SQLite with pre-calculated per-game columns (PPG, APG, RPG, etc.). `scrape_bios.py` scrapes Wikipedia for biographical info, and `build_vectorstore.py` chunks and embeds the bios into ChromaDB.

2. **Agent Routing**: The agent uses LangGraph's ReAct pattern. When a user asks a question, the LLM reads the tool descriptions and decides whether to use the SQL toolkit (for statistical queries like "LeBron's PPG last 5 years") or the vector search tool (for biographical queries like "How many championships has Curry won?").

3. **System Prompt**: Business rules in the system prompt handle edge cases like team abbreviation mapping, special character normalization in player names, minimum attempt thresholds for percentage stats, and awareness of the latest season for relative time queries.

## Setup

### Prerequisites

- Python 3.10+
- OpenAI API key

### Installation

```bash
# Clone the repository
git clone https://github.com/bryanchuu/nba-rag-agent.git
cd nba-rag-agent

# Install dependencies
pip install langchain langchain-openai langchain-chroma langchain-community langgraph
pip install streamlit chromadb nba_api beautifulsoup4 requests python-dotenv unidecode

# Set up environment variables
echo "OPENAI_API_KEY=your_key_here" > .env
```

### Build the Data

Run these in order:

```bash
# 1. Pull NBA stats and build SQLite database
python setup_db.py

# 2. Scrape Wikipedia bios for top 500 scorers
python scrape_bios.py

# 3. Build ChromaDB vector store from bios
python build_vectorstore.py
```

> **Note**: `setup_db.py` pulls 40 seasons of data and may take several minutes. `scrape_bios.py` scrapes ~500 Wikipedia pages and also takes some time.

## Usage

### Streamlit UI (Recommended)

```bash
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

### Terminal Mode

```bash
python rag_agent.py
```

## Example Questions

**Statistical (SQL)**:
- "Who scored the most points in 2023-24?"
- "Give me LeBron James' average points per game last 5 years"
- "Which players had a free throw percentage above 90% last season?"

**Biographical (Vector Search)**:
- "How many championships has Stephen Curry won?"
- "Tell me about Nikola Jokic's career history"
- "What awards has Giannis Antetokounmpo won?"

## Database Details

- **18,390+ player-season records** across 40 seasons (1984-2025)
- **16 pre-calculated per-game columns**: PPG, APG, RPG, SPG, BPG, MPG, TOPG, FPG, FGA_PG, FGM_PG, FG3A_PG, FG3M_PG, FTA_PG, FTM_PG, OREB_PG, DREB_PG
- **PLAYER_NORMALIZED column** for ASCII-safe name matching
- **12,006 vector chunks** from 499 player biographies

