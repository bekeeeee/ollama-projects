from langchain.agents import initialize_agent, AgentType
from langchain.llms import Ollama
from tools.sql import run_query_tool
import logging

# Enable verbose logging
logging.basicConfig(level=logging.INFO)

# Initialize Ollama 
llm = Ollama(model="llama3", temperature=0)

# Initialize agent
agent = initialize_agent(
    tools=[run_query_tool],
    llm=llm,
    # agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    # verbose=True,
    handle_parsing_errors=True,
    max_iterations=3,
)

# Run with explicit instructions
question = """How many users?
You MUST use the run_sqlite_query tool with a properly formatted SQL query.
Return ONLY the count number."""

try:
    result = agent.run(question)
    print("\nFINAL RESULT:", result)
except Exception as e:
    print("Agent failed:", str(e))
