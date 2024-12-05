# Filename: intermediary_service.py

from fastapi import FastAPI, HTTPException
import httpx
import uvicorn
from dotenv import load_dotenv
import os

# Load .env file - because secrets are like your ex's social media, keep them hidden!
load_dotenv()

# Setup our cool FastAPI app - think of it like setting up your dating profile, but for APIs
app = FastAPI()

@app.post("/predict")
async def generate_image(prompt: dict):
    """
    This endpoint is where the magic happens - or at least where we try to make it happen. 
    It's like asking your AI friend to draw you something cool, but with less crayon.

    :param prompt: A dict containing your image request - think of it as your mood board for the AI
    :return: JSON response with your AI masterpiece or a sad error message if the AI's on a coffee break
    """
    try:
        # Get your Hugging Face token - it's like your VIP pass to the AI art world
        hf_token = os.getenv('HUGGING_FACE_TOKEN')
        # URL where our Flux 1 model lives - this is like the address to your favorite online store
        model_url = os.getenv('FLUX_1_URL') or "your-flux-1-endpoint-url"
        
        # Set up the headers like you're preparing for a fancy dinner party
        headers = {"Authorization": f"Bearer {hf_token}"}
        
        # This is where we actually ask the AI to do its thing
        response = await httpx.post(model_url, json=prompt, headers=headers)
        response.raise_for_status()  # If the AI throws a tantrum, we catch it here
        
        # Return the art, or the error if the AI decided to take a nap
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Failed to generate image - AI's got no chill today")

@app.post("/generate_video")
async def generate_video(prompt: dict):
    """
    Like asking your AI to make a TikTok video, but without the dance moves. 
    We're still working on getting the AI to do that moonwalk.

    :param prompt: Your video vibe - what's the plot of this short film?
    :return: JSON with your video or a message saying "video not found"
    """
    try:
        # Video generation is not implemented yet - imagine this like a placeholder for future awesomeness
        return {"status": "not implemented", "message": "Video generation coming soon™"}
    except Exception as e:
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
        raise HTTPException(status_code=400, detail="URL missing - where are we supposed to go?")
    
    try:
        # Here's where we actually send the friend request (HTTP POST)
        response = await httpx.post(url, json=data.get('payload', {}))
        response.raise_for_status()
        return {"status": "success", "data": response.json()}
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"API said nope - {e.response.text}")

if __name__ == "__main__":
    # Start the server - think of it as turning on your party lights
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")  # Choose your own port for this bash
