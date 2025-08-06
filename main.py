import google_search_api
import summarizer
import web_crawler
import LLM
import utils
import person_researcher
import json
import logging
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def research_query(query: str):
    # Step 1: Classify query type
    # try:
    #     query_classification = LLM.classify_query_type(query)
    #     query_type = query_classification.get("query_type")
    #     print(query_type)
    # except Exception as e:
    #     logging.error(f"Error classifying query type: {e}")
    #     return "Error: Could not classify query type."

    # if query_type == "person":
    #     person_name = query_classification.get("person_name")
    #     initial_context = query_classification.get("initial_context", "")
    #     logging.info(f"Detected person search for: {person_name} (Context: {initial_context})")
    #     try:
    #         person_profile = await person_researcher.research_person({"name": person_name, "known_for": initial_context}, search_duration_minutes=5) # Set a reasonable default duration
    #         logging.info("\n--- Final Person Profile ---")
    #         logging.info(json.dumps(person_profile, indent=2))
    #         return person_profile
    #     except Exception as e:
    #         logging.error(f"Error researching person {person_name}: {e}")
    #         return "Error: Could not complete person research."
    # else:
    #     logging.info("Detected general research query.")
        # 1. Enhance query
        try:
            enhanced_queries = LLM.enhance_query_into_two(query)
            logging.info(f"Enhanced Queries: {enhanced_queries}")
        except Exception as e:
            logging.error(f"Error enhancing query: {e}")
            return "Error: Could not enhance query."

        # 2. Perform Google Search for each enhanced query
        all_search_results = []
        for q in enhanced_queries:
            try:
                search_results = google_search_api.google_search_api(q, google_search_api.api_key, google_search_api.cx)
                if search_results and "error" not in search_results:
                    all_search_results.extend(search_results)
                else:
                    logging.warning(f"No search results or error for query '{q}': {search_results.get('error', 'Unknown error')}")
            except Exception as e:
                logging.error(f"Error performing Google search for '{q}': {e}")
        logging.info(f"Total Search Results: {len(all_search_results)}")

        if not all_search_results:
            return "No relevant search results found."

        # 3. Crawl and extract content from search results
        all_article_content = []
        for result in all_search_results:
            try:
                html_content = await web_crawler.get_page_content(result["link"])
                if html_content:
                    article_data = await web_crawler.extract_article_content_with_newspaper(html_content, result["link"])
                    if article_data and article_data["text"]:
                        all_article_content.append(article_data["text"])
                    else:
                        logging.warning(f"No article content extracted from {result['link']}")
            except Exception as e:
                logging.error(f"Error crawling {result['link']}: {e}")
        logging.info(f"Total Articles Crawled: {len(all_article_content)}")

        if not all_article_content:
            return "No article content could be extracted from search results."

        # 4. Summarize and synthesize the extracted information
        full_text_for_summary = "\n\n".join(all_article_content)
        
        # Truncate text if it's too long for the LLM
        truncated_text = utils.truncate_text_by_words(full_text_for_summary, 10000) # Adjust word limit as needed

        try:
            final_summary = summarizer.summarize_with_gemini(truncated_text)
            logging.info(f"Final Summary: {final_summary}")
            return final_summary
        except Exception as e:
            logging.error(f"Error summarizing content: {e}")
            return "Error: Could not summarize extracted content."

# if __name__ == "__main__":
    # user_query = input("Enter your research query: ")
    # asyncio.run(research_query(user_query))