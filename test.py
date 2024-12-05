import httpx

async def test_intermediary():
    intermediary_url = "YOUR_INTERMEDIARY_SERVICE_URL/predict"  # or whatever your endpoint is
    payload = {"prompt": "Test input for your model"}  # Adjust based on your intermediary's expected input

    async with httpx.AsyncClient() as client:
        response = await client.post(intermediary_url, json=payload)
        print(response.text)

import asyncio
asyncio.run(test_intermediary())
