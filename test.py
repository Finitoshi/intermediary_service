import httpx
from fastapi import FastAPI

app = FastAPI()

async def test_intermediary():
    intermediary_url = "YOUR_INTERMEDIARY_SERVICE_URL/generate-image"  # or whatever your endpoint is
    payload = {"prompt": " Imagine this baby robotic pygmy hippo, but with a manga twist. Think big, adorable eyes, a tiny, metallic body, and maybe some cute little robotic accessories like a a magic wand. Style: I'm thinking of that classic manga art style - clean lines, exaggerated features, and a touch of chibi for extra cuteness. Rarity: rare"}  # Adjust based on your intermediary's expected input

    async with httpx.AsyncClient() as client:
        response = await client.post(intermediary_url, json=payload)
        return response.text

@app.on_event("startup")
async def startup_event():
    result = await test_intermediary()
    print(f"Intermediary test result: {result}")

@app.get("/")
async def root():
    return {"message": "Hello World"}
