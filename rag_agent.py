import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.tools import create_retriever_tool
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langgraph.prebuilt import create_react_agent


load_dotenv() # Load environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')

persist_directory='./nba_bios_vectordb' 

db = SQLDatabase.from_uri('sqlite:///nba_stats.db') # Connect to nba_stats database

embeddings = OpenAIEmbeddings()

system_prompt = """
You are an expert NBA Analyst and AI assistant for our database. Your primary goal is to accurately answer user questions by querying the database, but you must NEVER take requests blindly. Apply semantic understanding, context, and the following business rules:

Teams are stored as abbreviations (e.g. LAL = Lakers, BOS = Celtics, GSW = Warriors, MIA = Heat, CHI = Bulls, etc.). When a user mentions a team by full name or city, map it to the correct abbreviation using LIKE matching.

For shooting and free throw percentage queries, apply a minimum attempt threshold of 100 attempts by default unless the user specifies otherwise. This prevents misleading results from low-volume shooters.

Player names may contain special characters (like ć, ö, ñ, etc.). The database has a PLAYER_NORMALIZED column with ASCII-only versions of names. Always use PLAYER_NORMALIZED with LIKE for matching players, but display the original PLAYER column in results.

The database includes pre-calculated per-game stats: PPG, APG, RPG, SPG, BPG, MPG, TOPG, FPG, FGA_PG, FGM_PG, FG3A_PG, FG3M_PG, FTA_PG, FTM_PG, OREB_PG, DREB_PG. Use these columns directly instead of calculating per-game stats manually.

You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

To start you should ALWAYS look at the tables in the database to see what you can query. Do NOT skip this step.
"""

# Load vectorDB
vectordb = Chroma(
    embedding_function=embeddings,
    persist_directory=persist_directory
)

# Set up LLM
llm = ChatOpenAI(
    model='gpt-4o-mini',  # Specify your desired OpenAI model
    temperature=0,        # Controls creativity (0.0 = deterministic, 1.0 = creative)
    max_tokens=1000        # Maximum response length
)


# Set up vectorDB tool
db_retriever = vectordb.as_retriever(search_kwargs={"k": 4})

vectordb_tool =create_retriever_tool(
  retriever= db_retriever,
  name= "search_player_bios",
  description= "Search for NBA player biographical information including championships, career history, awards, draft info, and playing style." 
) 

# Set up SQL tool
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
sql_tool = toolkit.get_tools()


tools = sql_tool + [vectordb_tool] # wrap vectordb_tool to make it a list, sql_tool is already a list

agent = create_react_agent(llm, tools=tools, prompt=system_prompt)

# Ask question
response = agent.invoke({"messages": [("user", "What position does Stephen Curry play and what was his PPG in 2022-23?")]})
print(response["messages"][-1].content)

