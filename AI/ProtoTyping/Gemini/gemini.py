import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI, ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, BaseMessage
from typing import List


print("Starting...")
print("Loading environment variables...")
load_dotenv()
print("Environment variables loaded.")
google_api_key = os.getenv("GOOGLE_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

print("Initializing LLM...")

# llm = GoogleGenerativeAI(
#     model="gemini-1.5-pro",
#     google_api_key=google_api_key,
#     streaming=True
# )

# llm = ChatGoogleGenerativeAI(
#     model="gemini-1.5-pro",
#     google_api_key=google_api_key,
#     streaming=True
# )



input("Press Enter to continue...")

llm = ChatOpenAI(
    model="chatgpt-4o-latest",
    openai_api_key=openai_api_key,
    streaming=True
)

print("LLM initialized.")

print("Setting up messages...")
prompt = HumanMessage(content="Could you explain the BM25 algorithm and how it is used in RAG (Retrieval Augmented Generation) powered LLM applications?")
messages: List[BaseMessage] = [
    prompt
]
print("Messages set up.")
print(f"Proceeding to stream...\n{'-' * 80}")

print(f"{prompt.pretty_print()}\n")
def stream(messages: List[BaseMessage]):
    for i, chunk in enumerate(llm.stream(messages)):
        # Print without new line and flush immediately
        if i == 0:
            chunk.pretty_print()
        print(chunk.content, end="", flush=True)

stream(messages)
print(f"{'-' * 80}\n\nStream finished.")