import os
from dotenv import load_dotenv
import asyncio
from pymongo import MongoClient
from solana.rpc.api import Client
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import httpx

# Load .env file
load_dotenv()

# Setting up environment variables
BITTY_TOKEN_ADDRESS = os.getenv('BITTY_TOKEN_ADDRESS')
GROK_API_KEY = os.getenv('GROK_API_KEY')
GROK_API_URL = os.getenv('GROK_API_URL')
HF_INTERMEDIARY_TOKEN = os.getenv('HF_INTERMEDIARY_TOKEN')
HUGGINGFACE_API_TOKEN = os.getenv('HUGGINGFACE_API_TOKEN')
HUGGINGFACE_SPACE_URL = os.getenv('HUGGINGFACE_SPACE_URL')
INTERMEDIARY_URL = os.getenv('INTERMEDIARY_URL')
JWK_PATH = os.getenv('JWK_PATH')
MONGO_URI = os.getenv('MONGO_URI')
PORT = os.getenv('PORT')
RENDER_INTERMEDIARY_URL = os.getenv('RENDER_INTERMEDIARY_URL')
RENDER_TG_BOT_WEBHOOK_URL = os.getenv('RENDER_TG_BOT_WEBHOOK_URL')
SOLANA_RPC_URL = os.getenv('SOLANA_RPC_URL')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Check if all necessary variables are set
necessary_vars = ['TELEGRAM_BOT_TOKEN', 'GROK_API_KEY', 'MONGO_URI', 'SOLANA_RPC_URL']
for var in necessary_vars:
    if not os.getenv(var):
        raise ValueError(f"Environment variable {var} not set.")

# MongoDB setup
mongo_client = MongoClient(MONGO_URI)
db = mongo_client['your_database_name']
collection = db['your_collection_name']

# Solana RPC client setup
solana_client = Client(SOLANA_RPC_URL)

# Telegram Bot setup
application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Async function for AI interaction (Grok)
async def grok_interaction(prompt):
    headers = {"Authorization": f"Bearer {GROK_API_KEY}"}
    async with httpx.AsyncClient() as client:
        response = await client.post(GROK_API_URL, json={"prompt": prompt}, headers=headers)
        response.raise_for_status()
    return response.json()

# Example command for Telegram bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! I am an AI-powered Telegram bot!')

async def grok_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        response = await grok_interaction(' '.join(context.args))
        await update.message.reply_text(response.get('response', 'AI is thinking...'))
    else:
        await update.message.reply_text("Please provide a prompt for Grok to respond to.")

# Adding handlers to the Telegram bot
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("grok", grok_command))

# Example of using Hugging Face Space (this would be much more involved in real use)
async def hf_interaction():
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(HUGGINGFACE_SPACE_URL, headers=headers)
        return response.json()

async def main():
    print("Starting the bot...")
    
    # Example of database interaction
    collection.insert_one({"message": "Bot started"})

    # Example of Solana interaction
    result = solana_client.get_balance(BITTY_TOKEN_ADDRESS)
    print(f"Balance for {BITTY_TOKEN_ADDRESS}: {result['result']['value']}")

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
