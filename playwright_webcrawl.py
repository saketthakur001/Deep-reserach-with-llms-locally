from playwright.sync_api import sync_playwright
import random
import time
from newspaper import Article
import newspaper

def extract_article_content(html_content, url):
    """
    Extract the main article content from HTML using newspaper4k.
    
    :param html_content: HTML content of the page
    :param url: URL of the page (used for article initialization)
    :return: Dictionary containing article title, text, summary, and keywords
    """
    # Create an Article object
    article = Article(url)
    
    # Instead of downloading, we'll set the html directly
    article.html = html_content
    
    # Parse the article
    article.parse()
    
    # NLP processing for summary and keywords
    try:
        article.nlp()
        summary = article.summary
        keywords = article.keywords
    except Exception as e:
        summary = "Summary extraction failed"
        keywords = []
    
    # Return a dictionary with the article details
    return {
        "title": article.title,
        "text": article.text,
        "summary": summary,
        "keywords": keywords,
        "publish_date": article.publish_date
    }




def get_page_articles(url, headless=True):
    """
    Fetches and returns relevant article content from a webpage using Playwright and newspaper4k.
    
    :param url: The URL of the page to fetch.
    :param headless: Whether to run in headless mode (default is True).
    :return: Dictionary containing article information.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        
        #add some randomization to seem more human-like
        page.set_viewport_size({"width": 1366, "height": 768})
        
        #go to the URL
        page.goto(url, timeout=60000)
        
        #2ait for the page to load completely
        page.wait_for_load_state("networkidle")
        
        #get the full html content
        html_content = page.content()

        #save the html content to a file
        with open("html_content.html", "w") as file:
            file.write(html_content)
        
        # Extract article content using newspaper4k
        article_content = extract_article_content(html_content, url)
        
        # Close the browser
        browser.close()
        
        return article_content

def get_articles_from_source(source_url, max_articles=5, headless=True):
    print("it's working now")
    source = newspaper.build(source_url, memoize_articles=False)
    
    #getting article URLs
    article_urls = [article.url for article in source.articles[:max_articles]]
    
    #content for each article
    articles = []
    for url in article_urls:
        try:
            article_content = get_page_articles(url, headless)
            articles.append(article_content)
            #delay
            time.sleep(random.uniform(1, 3))
        except Exception as e:
            print(f"Error processing {url}: {e}")
    
    return articles

if __name__ == "__main__":
    # Test single article extraction
    url = "https://en.wikipedia.org/wiki/Meaning_of_life"
    article = get_page_articles(url, headless=True)
    print(f"Title: {article['title']}")
    print(f"Text (first 300 chars): {article['text'][:3000]}...")
    print(f"Summary: {article['summary'][:3000]}...")
    print(f"Keywords: {article['keywords']}")
    print("\n" + "-"*50 + "\n")
    
    # # Test multiple articles from a source
    # news_source = "https://www.bbc.com/news"
    # print(f"Getting articles from {news_source}...")
    # articles = get_articles_from_source(news_source, max_articles=3, headless=True)

    # for i, article in enumerate(articles, 1):
    #     print(f"Article {i}:")
    #     print(f"Title: {article['title']}")
    #     print(f"Text (first 200 chars): {article['text'][:2000]}...")
    #     print("\n")


# from playwright.sync_api import sync_playwright
# import random
# import time


# def get_page_text(url, headless=True):
#     """
#     Fetches and returns all visible text from a webpage using Playwright.
    
#     :param url: The URL of the page to fetch.
#     :param headless: Whether to run in headless mode (default is True).
#     :return: The text content of the page.
#     """
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=headless)
#         page = browser.new_page()
#         page.goto(url, timeout=60000)
#         page_text = page.inner_text("body")  # Extract all visible text
#         browser.close()
#         return page_text


# if __name__ == "__main__":
#     # test
#     url = "https://en.wikipedia.org/wiki/Meaning_of_life#Questions"
#     # print(get_page_text(url, headless=False))  # Run in normal mode
#     print(get_page_text(url, headless=True))   # Run in headless mode
