from fastapi import FastAPI, HTTPException
import httpx
import uvicorn
from dotenv import load_dotenv
import os
import logging
import asyncio  # Because sometimes you need to wait for the AI to think

# Setup logging - because if you're not logging, are you even coding?
logging.basicConfig(
    level=logging.DEBUG,  # We're setting it to DEBUG for those who want to see everything... literally everything
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("IntermediaryService")
logger.debug("Setting up the logger - We're going to log so much, you'll need a bigger screen!")

# Load .env - secrets are like your diary, only share with your best friend (the AI)
load_dotenv()

# Initialize our fancy FastAPI app - it's like starting a new band, but with code
app = FastAPI()

# Here's where the magic happens (or at least where we try to make it happen)
@app.post("/predict")
async def generate_image(prompt: dict):
    """
    This endpoint is like asking your AI buddy to paint you a picture. 
    But remember, AI's taste in art might be... interesting.

    :param prompt: A dict containing your image request - think of it as your mood board for the AI
    :return: JSON response with your AI masterpiece or a sad error message if the AI's creativity tank is empty
    """
    logger.info(f"👀 Got a request to generate an image with prompt: {prompt}")
    
    try:
        # Grab your Hugging Face token - it's like your backstage pass to the AI art gallery
        hf_token = os.getenv('HUGGING_FACE_TOKEN')
        if not hf_token:
            logger.error("🤦 No Hugging Face token found! Are we gatecrashing?")
            raise HTTPException(status_code=401, detail="No Hugging Face token provided - Access Denied!")
        
        # URL where our Flux 1 model lives - this is like the address to your favorite online store
        model_url = os.getenv('FLUX_1_URL') or "your-flux-1-endpoint-url"
        
        # Set up the headers like you're preparing for a fancy dinner party
        headers = {"Authorization": f"Bearer {hf_token}"}
        
        logger.debug(f"🔑 Authenticating with token: {hf_token[:5]}...{hf_token[-5:] if hf_token else 'No token'}")
        logger.debug(f"🌐 Connecting to model at: {model_url}")
        
        # This is where we actually ask the AI to do its thing
        async with httpx.AsyncClient() as client:
            response = await client.post(model_url, json=prompt, headers=headers)
        logger.debug(f"HTTP Response Status: {response.status_code}")
        response.raise_for_status()  # If the AI throws a tantrum, we catch it here
        
        logger.info(f"🎉 Successfully generated image! AI did the thing!")
        return response.json()
    except httpx.HTTPStatusError as e:
        logger.warning(f"😤 AI didn't feel like generating an image today. Status code: {e.response.status_code}")
        logger.debug(f"Response Text: {e.response.text[:100]}...")  # Just the first 100 chars to save space
        raise HTTPException(status_code=e.response.status_code, detail="Failed to generate image - AI's got no chill today")
    except Exception as e:
        logger.error(f"💥 Whoops! Something went wrong with image generation:", exc_info=True)
        raise HTTPException(status_code=500, detail="Something went boom. Try again later!")

@app.post("/generate_video")
async def generate_video(prompt: dict):
    """
    Like asking your AI to make a TikTok video, but without the dance moves. 
    We're still working on getting the AI to do that moonwalk.

    :param prompt: Your video vibe - what's the plot of this short film?
    :return: JSON with your video or a message saying "video not found"
    """
    logger.info(f"📹 Got a request to generate a video with prompt: {prompt}")
    
    try:
        # Video generation is not implemented yet - imagine this like a placeholder for future awesomeness
        logger.info("🚧 Video generation feature under construction...")
        logger.debug("Returning placeholder response for now.")
        return {"status": "not implemented", "message": "Video generation coming soon™"}
    except Exception as e:
        logger.error(f"🎥 Video generation crashed -", exc_info=True)
        raise HTTPException(status_code=500, detail="The video AI is lost in the sauce")

@app.post("/api_call")
async def make_api_call(data: dict):
    """
    This is your AI's way of making friends with other APIs. It's like networking, but for computers.

    :param data: Contains 'url' and 'payload' - think of it as sending a friend request with a custom message
    :return: The response from the other API or a message saying "friendship request failed"
    """
    url = data.get('url')
    if not url:
        logger.warning("🤔 Trying to make an API call without a URL. That's like DMing without a username.")
        raise HTTPException(status_code=400, detail="URL missing - where are we supposed to go?")
    
    logger.info(f"🤝 Attempting to connect to {url} with payload: {data.get('payload', {})}")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data.get('payload', {}))
        logger.debug(f"API Response Status: {response.status_code}")
        response.raise_for_status()
        logger.info(f"🎉 API call successful! We've made a new friend.")
        return {"status": "success", "data": response.json()}
    except httpx.HTTPStatusError as e:
        logger.warning(f"😞 API didn't want to be our friend. Status code: {e.response.status_code}")
        logger.debug(f"Response Text: {e.response.text[:100]}...")  # Just the first 100 chars to save space
        raise HTTPException(status_code=e.response.status_code, detail=f"API said nope - {e.response.text}")
    except Exception as e:
        logger.error(f"💣 API call exploded -", exc_info=True)
        raise HTTPException(status_code=500, detail="Something went wrong with the API handshake.")

if __name__ == "__main__":
    # Start the server - think of it as turning on your party lights
    logger.info("🚀 Starting the Intermediary Service - Let's get this party started!")
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")  # Choose your own port for this bash
