import requests

# URL for the Hugging Face model API
API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"

# Your Hugging Face API token
API_TOKEN = ""  # Replace with your actual token or fetch from environment variables

# Headers for the request
headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# Data to send in the request body
payload = {
    "inputs": "Imagine this baby robotic pygmy hippo, but with a manga twist. Think big, adorable eyes, a tiny, metallic body, and maybe some cute little robotic accessories like a a mini jetpack. Style: I'm thinking of that classic manga art style - clean lines, exaggerated features, and a touch of chibi for extra cuteness. Rarity: rare"
}

# Make the POST request
response = requests.post(API_URL, headers=headers, json=payload)

# Check if the request was successful
if response.status_code == 200:
    # Assuming the response is an image or some binary data, save or process it
    with open('astronaut_horse.png', 'wb') as file:
        file.write(response.content)
    print("Image saved successfully!")
else:
    print(f"Request failed with status code: {response.status_code}")
    print(response.text)  # This will print the error message if any
