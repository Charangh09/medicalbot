from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# ✅ Load environment variables first
load_dotenv()

# Debug: print to ensure keys are loaded
print("🔑 GROQ_API_KEY loaded:", os.getenv("GROQ_API_KEY")[:8] if os.getenv("GROQ_API_KEY") else "❌ Not Found")
print("🔑 PINECONE_API_KEY loaded:", os.getenv("PINECONE_API_KEY")[:8] if os.getenv("PINECONE_API_KEY") else "❌ Not Found")
print("🔑 TAVILY_API_KEY loaded:", os.getenv("TAVILY_API_KEY")[:8] if os.getenv("TAVILY_API_KEY") else "❌ Not Found")

# ✅ Import after loading env vars
from agentbot.agent import rag_agent
from agentbot.backend.vectorstore import add_document_to_vectorstore

# Initialize FastAPI
app = FastAPI(title="Main Project RAG Backend")

# Allow CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict later to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root route for testing
@app.get("/")
async def root():
    return {"message": "Hello from main-project!"}

# ✅ Chat endpoint
@app.post("/chat/")
async def chat_with_agent(query: str):
    try:
        response = rag_agent.chat(query)
        return {"response": response}
    except Exception as e:
        print("Error in chat_with_agent:", e)
        return {"error": str(e)}

# ✅ Upload document endpoint
@app.post("/upload/")
async def upload_document(file: UploadFile = File(...)):
    try:
        file_path = os.path.join("data", file.filename)
        os.makedirs("data", exist_ok=True)

        with open(file_path, "wb") as f:
            f.write(await file.read())

        add_document_to_vectorstore(file_path)
        return {"message": f"File '{file.filename}' uploaded successfully and added to vectorstore."}
    except Exception as e:
        print("Error in upload_document:", e)
        return {"error": str(e)}
