from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Access environment variables
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
CLIENT_ID = os.getenv('CLIENT_ID')
