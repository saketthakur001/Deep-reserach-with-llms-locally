import google_search_api
import summarizer
import web_crawler
import LLM
import utils
import person_researcher
import json

def research_query(query: str):
    # Step 1: Classify query type
    query_classification = LLM.classify_query_type(query)
    query_type = query_classification.get("query_type")

    if query_type == "person":
        person_name = query_classification.get("person_name")
        initial_context = query_classification.get("initial_context", "")
        print(f"Detected person search for: {person_name} (Context: {initial_context})")
        person_profile = person_researcher.research_person({"name": person_name, "known_for": initial_context}, search_duration_minutes=5) # Set a reasonable default duration
        print("\n--- Final Person Profile ---")
        print(json.dumps(person_profile, indent=2))
        return person_profile
    else:
        print("Detected general research query.")
        # 1. Enhance query
        enhanced_queries = LLM.enhance_query_into_two(query)
        print(f"Enhanced Queries: {enhanced_queries}")

        # 2. Perform Google Search for each enhanced query
        all_search_results = []
        for q in enhanced_queries:
            search_results = google_search_api.google_search_api(q, google_search_api.api_key, google_search_api.cx)
            if search_results and "error" not in search_results:
                all_search_results.extend(search_results)
        print(f"Total Search Results: {len(all_search_results)}")

        # 3. Crawl and extract content from search results
        all_article_content = []
        for result in all_search_results:
            try:
                html_content = web_crawler.get_page_content(result["link"])
                article_data = web_crawler.extract_article_content_with_newspaper(html_content, result["link"])
                all_article_content.append(article_data["text"])
            except Exception as e:
                print(f"Error crawling {result['link']}: {e}")
        print(f"Total Articles Crawled: {len(all_article_content)}")

        # 4. Summarize and synthesize the extracted information
        full_text_for_summary = "\n\n".join(all_article_content)
        
        # Truncate text if it's too long for the LLM
        truncated_text = utils.truncate_text_by_words(full_text_for_summary, 10000) # Adjust word limit as needed

        final_summary = summarizer.summarize_with_local_llm(truncated_text)
        print(f"Final Summary: {final_summary}")

        return final_summary

if __name__ == "__main__":
    user_query = input("Enter your research query: ")
    research_query(user_query)
