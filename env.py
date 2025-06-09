from dotenv import load_dotenv
import os

def load_env():
    load_dotenv()
    required_vars = ['OPENROUTER_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
