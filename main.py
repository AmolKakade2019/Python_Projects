from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.tools import tool  # tool decorator for defining functions as LangChain tools
from tools import get_current_time, WriteToFile, duckSearch, wikiSearchTool  # Importing user-defined tools
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

def main():
    response = "Query not sent!"
    global agent_executor, agent, prompt, parser, llm
    initialize()
    # Register the example tools with the agent
    tool_list = [get_current_time, WriteToFile, duckSearch, wikiSearchTool]
    agent = create_tool_calling_agent(llm, tools=tool_list, prompt=prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tool_list, verbose=True)
    question = "Who is chancellor of Germany? Provide sources for your answer and save it to a new file named 'Answer.txt' along with sources and tools used and tell path of this file."
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