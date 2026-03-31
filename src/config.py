import os
from dotenv import load_dotenv
from google import genai
import videodb

# Load environment variables
load_dotenv()

# Extract Keys
VIDEO_DB_API_KEY = os.getenv("VIDEO_DB_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

def init_clients():
    """Validates keys and returns API clients for the agents."""
    if not VIDEO_DB_API_KEY or not GEMINI_API_KEY:
        raise ValueError("Missing Required API Keys. Please check your .env file.")
        
    # Initialize Gemini using google-genai
    gemini_client = genai.Client(api_key=GEMINI_API_KEY)
    
    # Initialize VideoDB
    videodb.connect(api_key=VIDEO_DB_API_KEY)
    
    return gemini_client

GEMINI_CLIENT = None

def get_gemini():
    global GEMINI_CLIENT
    if not GEMINI_CLIENT:
        GEMINI_CLIENT = init_clients()
    return GEMINI_CLIENT
