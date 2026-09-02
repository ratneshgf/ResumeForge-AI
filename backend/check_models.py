"""Check available Gemini models"""
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("Available Gemini models:")
print("-" * 50)

try:
    models = client.models.list()
    for model in models:
        # Check if it supports generateContent
        if hasattr(model, 'supported_generation_methods'):
            methods = model.supported_generation_methods
        else:
            methods = ["unknown"]
        
        print(f"Name: {model.name}")
        if hasattr(model, 'display_name'):
            print(f"Display: {model.display_name}")
        if hasattr(model, 'description'):
            print(f"Description: {model.description[:100] if model.description else 'N/A'}")
        print(f"Methods: {methods}")
        print("-" * 50)
except Exception as e:
    print(f"Error listing models: {e}")
