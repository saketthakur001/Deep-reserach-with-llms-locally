import json
import keyring
from llama_cpp import Llama
import logging
import google.generativeai as genai # Import genai for configure
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='myapp.log')

# Local LLM initialization (kept for fallback)
llm = Llama.from_pretrained(
    repo_id="unsloth/gemma-3-1b-it-GGUF",
    filename="gemma-3-1b-it-Q5_K_M.gguf",
    n_ctx=20000
)

def _get_gemini_model():
    try:
        api_key = keyring.get_password("gemini_key", "user1")
        if not api_key:
            logging.warning("GEMINI_API_KEY not found in keyring. Falling back to local LLM.")
            return None
        genai.configure(api_key=api_key) # Still need this for other modules that might use genai directly
        return ChatGoogleGenerativeAI(model="gemma-3-12b-it", google_api_key=api_key) # gemini-pro is paid so always use gemma-3-12b-it
    except Exception as e:
        logging.error(f"Error configuring Gemini API: {e}. Falling back to local LLM.")
        return None

def enhance_query_into_two(query: str) -> list:
    gemini_model = _get_gemini_model()
    if gemini_model:
        try:
            logging.info("Using Gemini for query enhancement.")
            prompt = (
                f"Rewrite the following search query into multiple improved versions. "
                f"If the query is complex, break it into two or multiple separate queries that capture its different aspects.\n\n"
                f"Query: {query}\n\n"
                f"Provide all variations, each on a new line."
                f"example:- this is an example query"
            )
            response = gemini_model.invoke([HumanMessage(content=prompt)])
            queries = response.content.strip().split("\n")
            return [q.strip("- ").strip("* ").strip() for q in queries if q.strip()]
        except Exception as e:
            logging.error(f"Gemini query enhancement failed: {e}. Falling back to local LLM.")

    logging.info("Using local LLM for query enhancement.")
    prompt = (
        f"Rewrite the following search query into multiple improved versions. "
        f"If the query is complex, break it into two or multiple separate queries that capture its different aspects.\n\n"
        f"Query: {query}\n\n"
        f"Provide all variations, each on a new line."
        f"example:- this is an example query"
    )
    response = llm.create_chat_completion(messages=[{"role": "user", "content": prompt}])
    queries = response["choices"][0]["message"]["content"].strip().split("\n")[2:]
    return [q.strip("- ").strip("* ").strip() for q in queries if q.strip()]

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

#standard python entry point
if __name__ == "__main__":
    #testinng enhanced query
    print(enhance_query_into_two('why do cats don\'t spill their milk?'))
    print(classify_query_type("Tell me about Elon Musk, the CEO of Tesla."))
    print(classify_query_type("What is the capital of France?"))