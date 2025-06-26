# using quantized models with llama_cpp
from llama_cpp import Llama
import json

#quantized model from hugging face
# make sure the model file is in the same directory or provide the full path context widnow max
llm = Llama.from_pretrained(
    repo_id="unsloth/gemma-3-1b-it-GGUF",
    filename="gemma-3-1b-it-Q5_K_M.gguf",
    n_ctx=20000
    )

def enhance_query_into_two(query: str) -> list:
    prompt = (
        f"Rewrite the following search query into multiple improved versions. "
        f"If the query is complex, break it into two or multiple separate queries that capture its different aspects.\n\n"
        f"Query: {query}\n\n"
        f"Provide all variations, each on a new line."
        f"example:- this is an example query"
    )
    
    response = llm.create_chat_completion(messages=[{"role": "user", "content": prompt}])
    #The response might include bullet points or other formatting, so we do a basic cleanup:
    queries = response["choices"][0]["message"]["content"].strip().split("\n")[2:]
    return [q.strip("- ").strip("* ").strip() for q in queries if q.strip()]

def classify_query_type(query: str) -> dict:
    """
    Classifies the query as a 'person' search or 'general' research.
    If 'person', it extracts the person's name and any initial context.
    """
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
        print(f"Warning: Could not parse LLM response for query classification: {response_text}")
        return {"query_type": "general"}

#standard python entry point
if __name__ == "__main__":
    #testinng enhanced query
    print(enhance_query_into_two('why do cats don\'t spill their milk?'))
    print(classify_query_type("Tell me about Elon Musk, the CEO of Tesla."))
    print(classify_query_type("What is the capital of France?"))
