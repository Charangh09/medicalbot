import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

# Load .env from the project root (two levels up from this file) to ensure
# variables are available whether uvicorn is started from the project root
# or the backend folder. Fall back to find_dotenv() if that path isn't found.
base_dir = Path(__file__).resolve().parent.parent
dotenv_path = base_dir / '.env'
if dotenv_path.exists():
	load_dotenv(dotenv_path=str(dotenv_path))
else:
	# Fallback: let python-dotenv try to find a .env automatically
	load_dotenv(find_dotenv())

# Pinecone
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT","us-east-1") 
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "rag-index") 

# Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Tavily
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Embedding Model
EMBED_MODEL = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

# Paths (adjust as needed)
DOC_SOURCE_DIR = os.getenv("DOC_SOURCE_DIR", "data")