import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NGROK_URL = os.getenv("NGROK_URL")
PDF_CONTEXT_PATH = os.getenv("PDF_CONTEXT_PATH", "context_document.pdf")

