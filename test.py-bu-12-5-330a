import os
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler
import requests
from pymongo import MongoClient

# Setup logging - because if your code isn't talking to you, are you even friends?
logging.basicConfig(
    level=logging.DEBUG,  # Let's be detectives. Everything gets logged!
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Here's our main gossip - the logger
logger = logging.getLogger(__name__)

# This little guy will make sure our log files don't grow into novels
file_handler = RotatingFileHandler('app.log', maxBytes=1000000, backupCount=3)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

# Load .env - because secrets are like your diary, keep 'em locked up!
load_dotenv()

# Environment variables - like your digital wardrobe, but for API keys
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
GROK_API_KEY = os.getenv('GROK_API_KEY')
GROK_API_URL = os.getenv('GROK_API_URL')
JWK_PATH = os.getenv('JWK_PATH')
HUGGINGFACE_API_TOKEN = os.getenv('HUGGINGFACE_API_TOKEN')
HUGGINGFACE_SPACE_URL = os.getenv('HUGGINGFACE_SPACE_URL')
RENDER_INTERMEDIARY_URL = os.getenv('RENDER_INTERMEDIARY_URL')
RENDER_TG_BOT_WEBHOOK_URL = os.getenv('RENDER_TG_BOT_WEBHOOK_URL')
MONGO_URI = os.getenv('MONGO_URI')
CHIBI_TG_KEY_GROK = os.getenv('CHIBI_TG_KEY_GROK')
HF_INTERMEDIARY_TOKEN = os.getenv('HF_INTERMEDIARY_TOKEN')

def setup_bot():
    if not TELEGRAM_BOT_TOKEN:
        logger.error("Telegram Bot Token is not set in the environment variables - No key, no party!")
        raise ValueError("Missing Telegram Bot Token")
    
    logger.info(f"Bot token starts with: {TELEGRAM_BOT_TOKEN[:5]}...")  # Only showing a peek, like a secret handshake
    # Here's where you'd actually start your bot if you had one
    logger.debug("Bot initialized - Watch out, world, we're now online!")

def hf_api_call():
    if not HUGGINGFACE_API_TOKEN:
        logger.error("Hugging Face API Token is not set in the environment variables - No hugs today!")
        raise ValueError("Missing Hugging Face API Token")
    
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"
    }
    logger.debug(f"Attempting to connect to Hugging Face Space: {HUGGINGFACE_SPACE_URL}")
    try:
        response = requests.get(HUGGINGFACE_SPACE_URL, headers=headers)
        response.raise_for_status()  # If this fails, we'll throw a tantrum
        logger.info(f"Successful API call to Hugging Face Space. Status code: {response.status_code}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error during Hugging Face API call: {e} - The internet must be mad at us")
        raise

def connect_to_mongo():
    if not MONGO_URI:
        logger.error("MongoDB URI is not set in the environment variables - Where's our data dungeon?")
        raise ValueError("Missing MongoDB URI")
    
    logger.debug("Attempting to connect to MongoDB - Knocking on the data door")
    try:
        client = MongoClient(MONGO_URI)
        db = client.get_default_database()
        logger.info("Successfully connected to MongoDB - We're in the club now!")
        return db
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e} - Looks like we're not on the guest list")
        raise

def grok_interaction(prompt):
    if not GROK_API_KEY or not GROK_API_URL:
        logger.error("Grok API key or URL is not set in the environment variables - Grok's gone silent!")
        raise ValueError("Missing Grok API credentials")
    
    headers = {"Authorization": f"Bearer {GROK_API_KEY}"}
    logger.debug(f"Making API call to Grok with prompt: {prompt[:50]}... - Asking Grok for wisdom")
    try:
        response = requests.post(GROK_API_URL, json={"prompt": prompt}, headers=headers)
        response.raise_for_status()  # If Grok doesn't answer, we'll know why
        logger.info(f"Successful Grok API call. Response status: {response.status_code}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error during Grok API call: {e} - Grok must be on coffee break")
        raise

if __name__ == "__main__":
    try:
        setup_bot()
        logger.debug("Calling Hugging Face API - Time for some digital hugging")
        hf_result = hf_api_call()
        logger.debug(f"Hugging Face API call result: {hf_result}")

        logger.debug("Connecting to MongoDB - Let's see if we can play with some data")
        mongo_db = connect_to_mongo()
        # Here's where we'd do something cool with MongoDB, like inserting a silly document
        mongo_db['test'].insert_one({"test": "document", "mood": "humorous"})

        logger.debug("Grok Interaction Test - Let's ask Grok something deep")
        grok_response = grok_interaction("What is the meaning of life?")
        logger.info(f"Grok response: {grok_response}")

    except Exception as e:
        logger.exception("An error occurred in the main execution - Everything's gone pear-shaped!")
