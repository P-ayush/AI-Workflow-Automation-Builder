from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

chat = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",   
    temperature=0,
    max_output_tokens=300
)
