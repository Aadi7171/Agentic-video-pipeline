import os
from dotenv import load_dotenv
from google import genai
import videodb

# Load environment variables once at import
load_dotenv()

VIDEO_DB_API_KEY = os.getenv("VIDEO_DB_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

# Lazily-initialized singletons
_gemini_client = None
_videodb_conn = None


def get_gemini() -> genai.Client:
    """Returns a cached Gemini client, creating it on first call."""
    global _gemini_client
    if _gemini_client is None:
        if not GEMINI_API_KEY:
            raise ValueError(
                "Missing GEMINI_API_KEY. Copy .env.example to .env and fill it in."
            )
        _gemini_client = genai.Client(api_key=GEMINI_API_KEY)
    return _gemini_client


def get_videodb():
    """Returns a cached VideoDB connection, creating it on first call."""
    global _videodb_conn
    if _videodb_conn is None:
        if not VIDEO_DB_API_KEY:
            raise ValueError(
                "Missing VIDEO_DB_API_KEY. Copy .env.example to .env and fill it in."
            )
        _videodb_conn = videodb.connect(api_key=VIDEO_DB_API_KEY)
    return _videodb_conn


def get_collection():
    """Returns the default VideoDB collection — the correct object to upload to."""
    return get_videodb().get_collection()
