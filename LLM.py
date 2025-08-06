import json
import logging
from llama_cpp import Llama
from google import genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='myapp.log')

# Variable for API/Local LLM selection
current_llm = "api"  # You can switch this to 'local' for local Llama model

# Define Llama model only if 'local' is selected
llm = None  # Start with no Llama model

if current_llm == 'local':
    try:
        # Only load Llama model if needed
        llm = Llama.from_pretrained(
            repo_id="unsloth/gemma-3-1b-it-GGUF",
            filename="gemma-3-1b-it-Q5_K_M.gguf",
            n_ctx=20000
        )
        logging.info("Local Llama model loaded.")
    except Exception as e:
        logging.error(f"Failed to load local Llama model: {e}")

def _get_gemini_model():
    try:
        if current_llm == 'api':
            api_key = os.getenv("GEMINI_KEY")
            print(api_key)
            if not api_key:
                logging.warning("GEMINI_API_KEY not found. Falling back to local LLM.")
                return None
            # Configure the unified client for Gemini
            client = genai.Client(api_key=api_key)
            return ChatGoogleGenerativeAI(model="gemma-3-12b-it", client=client)
        else:
            logging.warning("Using local LLM, Gemini API will not be called.")
            return None
    except Exception as e:
        logging.error(f"Error configuring GenAI SDK: {e}. Falling back to local LLM.")
        return None

def enhance_query_into_two(query: str) -> list:
    gemini_model = _get_gemini_model()
    print(gemini_model)
    if gemini_model:
        try:
            logging.info("Using Gemini for query enhancement.")
            prompt = (
                f"Rewrite the following search query into multiple improved versions. "
                f"If the query is complex, break it into two or multiple separate queries that capture its different aspects.\n\n"
                f"Query: {query}\n\n"
                f"Provide all variations, each on a new line."
            )
            response = gemini_model.invoke([HumanMessage(content=prompt)])
            print(response.content)
            queries = response.content.strip().split("\n")
            return [q.strip("- ").strip("* ").strip() for q in queries if q.strip()]
        except Exception as e:
            logging.error(f"Gemini query enhancement failed: {e}. Falling back to local LLM.")
    
    # If Gemini is not available, use local LLM
    if llm:
        logging.info("Using local LLM for query enhancement.")
        prompt = (
            f"Rewrite the following search query into multiple improved versions. "
            f"If the query is complex, break it into two or multiple separate queries that capture its different aspects.\n\n"
            f"Query: {query}\n\n"
            f"Provide all variations, each on a new line."
        )
        response = llm.create_chat_completion(messages=[{"role": "user", "content": prompt}])
        queries = response["choices"][0]["message"]["content"].strip().split("\n")[2:]
        return [q.strip("- ").strip("* ").strip() for q in queries if q.strip()]
    else:
        logging.warning("No LLM available for query enhancement.")
        return []

def classify_query_type(query: str) -> dict:
    gemini_model = _get_gemini_model()
    if gemini_model:
        try:
            logging.info("Using Gemini for query classification.")
            prompt = f"""Analyze the following query and determine if it is primarily a request for information about a specific person.
            If it is, extract the person's full name and any additional context provided about them (e.g., what they are known for).
            
            Query: {query}

            Provide the output in JSON format with 'query_type' (either "person" or "general").
            If 'query_type' is "person", also include 'person_name' and 'initial_context' (a string describing what they are known for).
            
            Example for person: {{\"query_type\": \"person\", \"person_name\": \"Marie Curie\", \"initial_context\": \"famous scientist, Nobel Prize winner\"}}
            Example for general: {{\"query_type\": \"general\"}}
            """
            response_text = gemini_model.invoke([HumanMessage(content=prompt)]).content.strip()
            return json.loads(response_text)
        except Exception as e:
            logging.error(f"Gemini query classification failed: {e}. Falling back to local LLM.")

    if llm:
        logging.info("Using local LLM for query classification.")
        prompt = f"""Analyze the following query and determine if it is primarily a request for information about a specific person.
        If it is, extract the person's full name and any additional context provided about them (e.g., what they are known for).
        
        Query: {query}

        Provide the output in JSON format with 'query_type' (either "person" or "general").
        If 'query_type' is "person", also include 'person_name' and 'initial_context' (a string describing what they are known for).
        
        Example for person: {{\"query_type\": \"person\", \"person_name\": \"Marie Curie\", \"initial_context\": \"famous scientist, Nobel Prize winner\"}}
        Example for general: {{\"query_type\": \"general\"}}
        """
        response_text = llm.create_chat_completion(messages=[{"role": "user", "content": prompt}])["choices"][0]["message"]["content"].strip()
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            logging.warning(f"Could not parse local LLM response for query classification: {response_text}")
            return {"query_type": "general"}

    logging.warning("No LLM available for query classification.")
    return {"query_type": "general"}

# standard python entry point
if __name__ == "__main__":
    # testing enhanced query
    print(enhance_query_into_two('why do cats don\'t spill their milk?'))
    # print(classify_query_type("Tell me about Elon Musk, the CEO of Tesla."))
    # print(classify_query_type("What is the capital of France?"))
