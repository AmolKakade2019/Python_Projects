from datetime import datetime, timezone  # For getting the current time in UTC
from langchain.tools import tool, Tool # tool decorator for defining functions as LangChain tools
from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun  # Example of an external tool
from langchain_community.utilities import WikipediaAPIWrapper
import os
# ---------------------------------------------------------------------------
# Langchain tool definitions that can be used by the agent
# ---------------------------------------------------------------------------
duckSearch = DuckDuckGoSearchRun()
duckSearchTool = Tool(
    name="DuckDuckGo_Search",
    func=duckSearch.run,
    description="Useful for when you need to look up current information on the internet. Input should be a search query."
)

WikiAPIWrapper = WikipediaAPIWrapper(top_k_results=3, doc_content_chars_max=1000)
wikiSearchTool = WikipediaQueryRun(api_wrapper=WikiAPIWrapper)
# ---------------------------------------------------------------------------
# user defined tool definitions that can be used by the agent
# ---------------------------------------------------------------------------

@tool
def get_current_time() -> str:
    """Return the current UTC time as an ISO‑8601 string."""
    return datetime.now(timezone.utc).isoformat()

@tool
def WriteToFile(text: str) -> str:
    """Write the provided text to a file and return the file path."""
    
    current_dir = os.getcwd()  # Ensure the current working directory is correct
    file_path = f"{current_dir}\\Answer.txt"
    with open(file_path, "w") as f:
        f.write(text)
    return file_path