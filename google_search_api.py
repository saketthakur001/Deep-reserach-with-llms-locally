# get the api key from here
#https://programmablesearchengine.google.com/controlpanel/all

import requests


# import keyring
# keyring.set_keyring(keyring.backends.null.Keyring())
# gemini_key = keyring.get_password("gemini_key", "user1")
# search_engine_id = keyring.get_password("search_engine_id", "user1")



from dotenv import load_dotenv
import os
load_dotenv()
gemini_key = os.getenv("GEMINI_KEY")
search_engine_id = os.getenv("SEARCH_ENGINE_ID")


# gemini_key = os.getenv("gemini_key")

def google_search_api(query, gemini_key, search_engine_id, num_results=10):
    """
    perform a google search using google custom search json api and return results.
    
    :param query: the search query.
    :param gemini_key: your google api key.
    :param search_engine_id: your google custom search engine id.
    :param num_results: number of results to fetch (default is 10).
    :return: list of search results with title, link, and snippet.
    """
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": gemini_key,
        "search_engine_id": search_engine_id,
        "num": num_results
    } 

    response = requests.get(url, params=params)
    data = response.json()
    
    #check if there are search results in the response
    if "items" in data:
        return [
            {
                "title": result.get("title"),
                "link": result.get("link"),
                "snippet": result.get("snippet")
            }
            for result in data["items"]
        ]
    else:
        return {"error": "no results found or invalid api key."}


#standard python entry point
if __name__ == "__main__":
    # Example usage:
    search_results = google_search_api('what is the meaning of life?', gemini_key, search_engine_id)
    if "error" in search_results:
        print(search_results["error"])
    else:
        for i, result in enumerate(search_results):
            print(f"Result {i+1}:")
            print(f"  Title: {result['title']}")
            print(f"  Link: {result['link']}")
            print(f"  Snippet: {result['snippet']}")
            print("\n")
