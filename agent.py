import os
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import create_sql_agent

load_dotenv() # Load environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(
    model='gpt-4o-mini',  # Specify your desired OpenAI model
    temperature=0,        # Controls creativity (0.0 = deterministic, 1.0 = creative)
    max_tokens=1000        # Maximum response length
)

db = SQLDatabase.from_uri('sqlite:///nba_stats.db') # Connect to nba_stats database
print(db.get_usable_table_names()) # Sanity check for tables in database


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

# Create SQL Agent
agent_executor = create_sql_agent( 
    llm=llm, 
    db=db,
    agent_type='tool-calling',
    prefix=system_prompt,
    verbose=True
)

# Ask question
question = "How many championships has LeBron James won?"
response = agent_executor.invoke({"input": question})

print("\nAnswer:")
print(response["output"])





