import time
import random
import json
from llama_cpp import Llama

import web_crawler
import google_search_api

# Initialize LLM (assuming it's a local model)
# This should ideally be passed or managed globally if multiple modules use it
llm = Llama.from_pretrained(
    repo_id="unsloth/gemma-3-1b-it-GGUF",
    filename="gemma-3-1b-it-Q5_K_M.gguf",
    n_ctx=20000
)

def _get_llm_response(prompt: str) -> str:
    """Helper function to get response from the local LLM."""
    response = llm.create_chat_completion(messages=[{"role": "user", "content": prompt}])
    return response["choices"][0]["message"]["content"].strip()

def _classify_person_type(initial_context: dict) -> dict:
    """
    Uses LLM to classify the person's type (e.g., famous, academic, professional)
    and suggest initial search keywords.
    """
    prompt = f"""Analyze the following initial context about a person and classify their likely type (e.g., "famous", "academic", "professional", "business", "local").
    Also, suggest initial relevant keywords for searching this person online.
    Initial context: {initial_context}

    Provide the output in a JSON format with 'person_type' and 'initial_keywords' (a list of strings).
    Example: {{\"person_type\": \"famous\", \"initial_keywords\": [\"actor\", \"movies\", \"Hollywood\"]}}
    """
    response_text = _get_llm_response(prompt)
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        print(f"Warning: Could not parse LLM response for person type classification: {response_text}")
        return {"person_type": "unknown", "initial_keywords": []}

def _generate_dynamic_search_queries(person_name: str, person_type: str, current_keywords: list) -> list:
    """
    Generates dynamic search queries based on person type and current keywords.
    Uses rule-based for common social media, LLM for more nuanced queries.
    """
    queries = []
    # Rule-based additions for common social media/platforms
    if person_type == "famous":
        queries.extend([
            f"{person_name} Instagram",
            f"{person_name} Facebook",
            f"{person_name} Twitter X.com",
            f"{person_name} official website"
        ])
    elif person_type == "academic":
        queries.extend([
            f"{person_name} university",
            f"{person_name} researchgate",
            f"{person_name} Google Scholar",
            f"{person_name} publications"
        ])
    elif person_type == "business":
        queries.extend([
            f"{person_name} LinkedIn",
            f"{person_name} company",
            f"{person_name} executive profile"
        ])
    
    # LLM-assisted query generation for more depth
    llm_prompt = f"""Given the person's name "{person_name}", their classified type "{person_type}", and current keywords {current_keywords},
    generate 3-5 additional, highly relevant and diverse search queries to find more information about them.
    Focus on unique identifiers, achievements, or specific affiliations.
    Provide each query on a new line.
    """
    llm_generated_queries = _get_llm_response(llm_prompt).split('\n')
    queries.extend([q.strip() for q in llm_generated_queries if q.strip()])
    
    # Add general queries
    queries.append(f"{person_name} biography")
    queries.append(f"{person_name} news")
    
    return list(set(queries)) # Remove duplicates

def _verify_identity_and_extract_facts(extracted_text: str, person_name: str, identity_fingerprint: dict) -> tuple[bool, dict]:
    """
    Uses LLM to verify if the extracted text is about the correct person and extracts new facts.
    identity_fingerprint: A dict of known facts like {'birth_year': '1980', 'occupation': 'actor'}
    """
    known_facts_str = ", ".join([f"{k}: {v}" for k, v in identity_fingerprint.items()]) if identity_fingerprint else "None"
    
    prompt = f"""Analyze the following text and determine if it is primarily about "{person_name}".
    Consider these known facts about the person for identity verification: {known_facts_str}.
    If it is the same person, extract any new, concrete facts (e.g., birth year, specific achievements, affiliations, social media handles) that can help confirm identity or build a profile.
    If it is a different person with a similar name, state that clearly.
    
    Text:
    {extracted_text[:1000]} # Limit text to avoid exceeding LLM context window

    Provide your response in JSON format with two keys:
    'is_same_person': true/false
    'new_facts': {{'fact_key': 'fact_value', ...}} (empty if not the same person or no new facts)
    'reason': 'brief explanation'
    
    Example for same person: {{\"is_same_person\": true, \"new_facts\": {{\"occupation\": \"scientist\", \"university\": \"MIT\"}}, \"reason\": \"Matches name and context\"}}
    Example for different person: {{\"is_same_person\": false, \"new_facts\": null, \"reason\": \"Different birth year and profession\"}}
    """
    response_text = _get_llm_response(prompt)
    try:
        llm_response = json.loads(response_text)
        return llm_response.get("is_same_person", False), llm_response.get("new_facts", {})
    except json.JSONDecodeError:
        print(f"Warning: Could not parse LLM response for identity verification: {response_text}")
        return False, {} # Default to not same person if parsing fails

def research_person(initial_context: dict, search_duration_minutes: int = 60) -> dict:
    """
    Conducts a detailed research on a person, verifying identity and accumulating information.
    
    Args:
        initial_context: A dictionary with initial info, e.g., {'name': 'John Doe', 'known_for': 'actor'}.
        search_duration_minutes: Maximum time to spend searching.
        
    Returns:
        A dictionary containing the compiled person profile.
    """
    person_name = initial_context.get("name")
    if not person_name:
        return {"error": "Person name is required in initial_context."}

    start_time = time.time()
    end_time = start_time + (search_duration_minutes * 60)

    # Step 1: Classify person type and get initial keywords
    classification_result = _classify_person_type(initial_context)
    person_type = classification_result.get("person_type", "unknown")
    current_keywords = classification_result.get("initial_keywords", [])
    
    print(f"Classified person type: {person_type}")
    print(f"Initial keywords: {current_keywords}")

    person_profile = {
        "name": person_name,
        "type": person_type,
        "summary": "",
        "details": {},
        "social_media": {},
        "links": [],
        "discrepancies": [],
        "confidence_score": 0
    }
    identity_fingerprint = {"name": person_name} # Key facts to verify identity

    urls_to_visit = []
    visited_urls = set()

    # Step 2: Initial search query generation and execution
    initial_queries = _generate_dynamic_search_queries(person_name, person_type, current_keywords)
    print(f"Initial search queries: {initial_queries}")

    for query in initial_queries:
        if time.time() > end_time:
            print("Search duration exceeded. Stopping initial searches.")
            break
        
        search_results = google_search_api.google_search_api(query, google_search_api.api_key, google_search_api.cx)
        if search_results and "error" not in search_results:
            for result in search_results:
                if result["link"] not in visited_urls:
                    urls_to_visit.append(result["link"])
                    visited_urls.add(result["link"])
        time.sleep(random.uniform(1, 3)) # Be polite

    print(f"Found {len(urls_to_visit)} unique URLs from initial searches.")

    # Step 3: Intelligent Crawling and Data Accumulation Loop
    while urls_to_visit and time.time() < end_time:
        url = urls_to_visit.pop(0)
        print(f"Processing URL: {url}")

        try:
            html_content = web_crawler.get_page_content(url)
            extracted_data = web_crawler.extract_article_content_with_newspaper(html_content, url)
            extracted_text = extracted_data.get("text", "")

            if not extracted_text:
                print(f"No main text extracted from {url}. Trying trafilatura...")
                extracted_text = web_crawler.extract_article_content_with_trafilatura(html_content)
            
            if not extracted_text:
                print(f"Still no text from {url}. Skipping.")
                continue

            # Identity Verification
            is_same_person, new_facts = _verify_identity_and_extract_facts(extracted_text, person_name, identity_fingerprint)

            if is_same_person:
                print(f"Confirmed identity for {url}. Extracting info...")
                # Update identity fingerprint
                identity_fingerprint.update(new_facts)
                
                # Extract detailed information using LLM
                extraction_prompt = f"""From the following text about "{person_name}", extract key details.
                Focus on: occupation, education, notable achievements, affiliations, social media handles (Instagram, Facebook, Twitter/X, LinkedIn), birth date/year, death date/year.
                Provide the output in JSON format. If a field is not found, omit it.
                Text:
                {extracted_text[:2000]} # Limit text for extraction
                """
                extracted_info_text = _get_llm_response(extraction_prompt)
                try:
                    extracted_info = json.loads(extracted_info_text)
                    person_profile["details"].update(extracted_info)
                    
                    # Special handling for social media links
                    for sm_platform in ["instagram", "facebook", "twitter", "linkedin"]:
                        if sm_platform in extracted_info:
                            person_profile["social_media"][sm_platform] = extracted_info[sm_platform]
                            del person_profile["details"][sm_platform] # Remove from general details
                            
                except json.JSONDecodeError:
                    print(f"Warning: Could not parse LLM response for info extraction: {extracted_info_text}")
                    # Add raw text to discrepancies if extraction fails
                    person_profile["discrepancies"].append(f"Failed to parse structured info from {url}: {extracted_info_text[:200]}")

                # Discover new links/keywords from the text
                discovery_prompt = f"""From the following text about "{person_name}", identify any new, relevant URLs or keywords that could lead to more information about THIS SAME PERSON.
                Provide URLs on new lines, followed by keywords on new lines.
                Text:
                {extracted_text[:1000]}
                """
                discovery_response = _get_llm_response(discovery_prompt)
                for line in discovery_response.split('\n'):
                    line = line.strip()
                    if line.startswith("http") and line not in visited_urls:
                        urls_to_visit.append(line)
                        visited_urls.add(line)
                    elif line and not line.startswith("http"):
                        current_keywords.append(line) # Add to keywords for future searches

            else:
                reason = new_facts.get("reason", "Identity not confirmed.")
                person_profile["discrepancies"].append(f"Skipped URL {url}: {reason}")
                print(f"Identity not confirmed for {url}. Reason: {reason}")

        except Exception as e:
            print(f"Error processing {url}: {e}")
            person_profile["discrepancies"].append(f"Error crawling {url}: {e}")
        
        time.sleep(random.uniform(1, 3)) # Be polite

    # Step 4: Data Consolidation and Synthesis
    final_synthesis_prompt = f"""Consolidate and synthesize the following raw extracted data about "{person_name}" into a comprehensive, well-structured profile.
    Resolve inconsistencies where possible, or list them under a 'discrepancies' section.
    Include a 'confidence_score' (0-100) based on the consistency and number of corroborating sources.
    
    Extracted Details: {person_profile["details"]}
    Social Media: {person_profile["social_media"]}
    Discrepancies encountered during search: {person_profile["discrepancies"]}
    Identity Fingerprint: {identity_fingerprint}

    Provide the final profile in JSON format with keys like:
    "name", "summary", "occupation", "education", "notable_achievements", "affiliations", "social_media_links" (dict), "birth_info", "death_info", "discrepancies", "confidence_score".
    """
    final_profile_text = _get_llm_response(final_synthesis_prompt)
    try:
        final_profile = json.loads(final_profile_text)
        person_profile.update(final_profile)
    except json.JSONDecodeError:
        print(f"Warning: Could not parse final LLM synthesis: {final_profile_text}")
        person_profile["summary"] = "Failed to synthesize a structured profile. Raw details: " + str(person_profile["details"])
        person_profile["confidence_score"] = 10 # Very low confidence

    return person_profile

if __name__ == "__main__":
    import json
    # Example Usage
    initial_person_context = {
        "name": "Elon Musk",
        "known_for": "entrepreneur, CEO of Tesla and SpaceX",
        "keywords": ["Tesla", "SpaceX", "Neuralink", "X.com"]
    }
    
    print(f"Starting research for {initial_person_context['name']}...")
    profile = research_person(initial_person_context, search_duration_minutes=1) # Set a short duration for testing
    
    print("\n--- Final Person Profile ---")
    print(json.dumps(profile, indent=2))
