import requests
import os

api_key = os.getenv("api_key")
cx = os.getenv("cx")


def google_search_api(query, api_key, cx, num_results=10):
    """
    Perform a Google search using Google Custom Search JSON API and return results.

    :param query: The search query.
    :param api_key: Your Google API key.
    :param cx: Your Google Custom Search Engine ID.
    :param num_results: Number of results to fetch (default is 10).
    :return: List of search results with title, link, and snippet.
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
        return {"error": "No results found or invalid API key."}

if __name__ == "__main__":
    # Example usagep
    print(google_search_api('what is the meaning of life?', api_key, cx))

