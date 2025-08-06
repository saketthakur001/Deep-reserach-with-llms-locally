import os
import logging
from google import genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Get API key from environment variables
api_key = os.getenv("GEMINI_KEY")

if not api_key:
    logging.error("GEMINI_API_KEY not found!")
else:
    try:
        # Initialize the Gemini client
        client = genai.Client(api_key=api_key)
        gemini_model = ChatGoogleGenerativeAI(model="gemma-3-12b-it", client=client)
        
        # Create a simple chat message to say "Hi"
        prompt = "Hi"
        response = gemini_model.invoke([HumanMessage(content=prompt)])
        
        # Print the response
        print(f"Gemini response: {response.content}")
        
    except Exception as e:
        logging.error(f"Error while communicating with Gemini API: {e}")
