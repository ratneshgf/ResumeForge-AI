"""Test which Gemini models are available and responding"""
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Models to test (free tier)
models_to_test = [
    "gemini-flash-latest",
    "gemini-3.7-flash",
    "gemini-3.6-flash", 
    "gemini-3.5-flash",
    "gemini-pro-latest",
    "gemini-flash-lite-latest",
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite"
]

print("Testing Gemini models for availability...\n")
print("=" * 60)

for model_name in models_to_test:
    try:
        print(f"\nTesting: {model_name}")
        
        generation_config = types.GenerateContentConfig(
            temperature=0.7,
            max_output_tokens=100,
            response_mime_type="application/json",
        )
        
        response = client.models.generate_content(
            model=model_name,
            contents="Return JSON: {\"test\": \"success\"}",
            config=generation_config,
        )
        
        if response.text:
            print(f"✅ SUCCESS - {model_name} is working!")
            print(f"   Response: {response.text[:50]}")
        else:
            print(f"❌ FAILED - Empty response")
            
    except Exception as e:
        error_str = str(e)
        if "503" in error_str or "UNAVAILABLE" in error_str:
            print(f"❌ FAILED - 503 Service Unavailable (high demand)")
        elif "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
            print(f"⚠️  RATE LIMITED - Too many requests")
        elif "404" in error_str or "NOT_FOUND" in error_str:
            print(f"❌ FAILED - Model not found or not available")
        else:
            print(f"❌ FAILED - {str(e)[:80]}")

print("\n" + "=" * 60)
print("\nTest complete!")
