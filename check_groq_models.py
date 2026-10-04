"""
Check which Groq models are available on your account
Run this to see what models you have access to
"""

import os
from dotenv import load_dotenv
from groq import Groq

# Load .env
load_dotenv()

# Get API key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("❌ GROQ_API_KEY not found in .env")
    exit(1)

print(f"✓ API Key found: {api_key[:10]}...")

# Create Groq client
client = Groq(api_key=api_key)

print("\n📋 AVAILABLE MODELS ON YOUR ACCOUNT:\n")

try:
    # List models
    models = client.models.list()
    
    for model in models.data:
        print(f"  • {model.id}")
    
    print(f"\n✓ Total models available: {len(models.data)}")
    
except Exception as e:
    print(f"❌ Error listing models: {e}")
    exit(1)