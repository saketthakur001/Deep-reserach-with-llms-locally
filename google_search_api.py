# get the api key from here
#https://programmablesearchengine.google.com/controlpanel/all

import requests
import keyring

api_key = keyring.get_password("gemini_key", "user1")
cx = keyring.get_password("search_engine_id", "user1")

# api_key = os.getenv("api_key")

def google_search_api(query, api_key, cx, num_results=10):
    """
    perform a google search using google custom search json api and return results.
    
    :param query: the search query.
    :param api_key: your google api key.
    :param cx: your google custom search engine id.
    :param num_results: number of results to fetch (default is 10).
    :return: list of search results with title, link, and snippet.
    """
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": api_key,
        "cx": cx,
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
    search_results = google_search_api('what is the meaning of life?', api_key, cx)
    if "error" in search_results:
        print(search_results["error"])
    else:
        for i, result in enumerate(search_results):
            print(f"Result {i+1}:")
            print(f"  Title: {result['title']}")
            print(f"  Link: {result['link']}")
            print(f"  Snippet: {result['snippet']}")
            print("\n")
