from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.tools import tool  # tool decorator for defining functions as LangChain tools
from datetime import datetime
import json

llm            = None
parser         = None
prompt         = None
agent          = None
agent_executor = None

class ClientResponse(BaseModel):
    topic: str
    sources: list[str]
    response: str
    tools_used: list[str]

def initialize():
    global llm, parser, prompt, agent, agent_executor
    load_dotenv()  # Load environment variables from .env file   
    #llm = ChatOllama(model="gemma3:1b", base_url="http://localhost:11434")
    llm = ChatOllama(model="gpt-oss:120b-cloud", base_url="https://ollama.com")
    llm_response = llm.invoke("who are you?")
    #print(llm_response)
    parser = PydanticOutputParser(pydantic_object=ClientResponse)
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template("""You are a helpful assistant that helps people in searching and coding tasks. 
                                              Answer the question by using the necessary tools and provide the sources for your answer. 
                                              Wrap the output in this format: \n {format_instructions}"""),
        ("placeholder", "{chat_history}"),
        HumanMessagePromptTemplate.from_template("{question}"),
        ("placeholder", "{agent_scratchpad}"),
        ]).partial(format_instructions=parser.get_format_instructions())
    
    # No additional initialization needed here
    pass

# ---------------------------------------------------------------------------
# Example tool definitions that can be used by the agent
# ---------------------------------------------------------------------------

@tool
def get_current_time() -> str:
    """Return the current UTC time as an ISO‑8601 string."""
    return datetime.utcnow().isoformat()

@tool
def echo(text: str) -> str:
    """Echo the provided text back unchanged."""
    return text

def main():
    response = "Query not sent!"
    global agent_executor, agent, prompt, parser, llm
    initialize()
    # Register the example tools with the agent
    tool_list = [get_current_time, echo]
    agent = create_tool_calling_agent(llm, tools=tool_list, prompt=prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tool_list, verbose=True)
    question = "is there active conflict between Afghanistan and Pakistan as of today? Provide sources for your answer and save answer to a new file named 'Answer.txt' and tell path of this file."
    response = agent_executor.invoke({"question": question})
    structured_response = parser.parse(response.get("output"))
    dict_response = json.loads(response.get("output"))
    print("Structured response:", structured_response)
    print("Dictionary response:")
    for item in dict_response.items():
        print(f"{item[0]}: {item[1]}\n")

if __name__ == "__main__":
    main()
    pass