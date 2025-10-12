from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_ollama import ChatOllama

load_dotenv()  # Load environment variables from .env file

#llm = ChatOllama(model="gemma3:1b", base_url="http://localhost:11434")
llm = ChatOllama(model="gpt-oss:120b-cloud", base_url="https://ollama.com")

response = llm.invoke("Write a poem about the sea.")
print(response)
