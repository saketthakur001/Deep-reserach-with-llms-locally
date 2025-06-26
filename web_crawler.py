from playwright.sync_api import sync_playwright
import random
import time
from newspaper import Article
import newspaper
import trafilatura

def extract_article_content_with_newspaper(html_content, url):
    """
    Extract the main article content from HTML using newspaper4k.
    
    :param html_content: HTML content of the page
    :param url: URL of the page (used for article initialization)
    :return: Dictionary containing article title, text, summary, and keywords
    """
    article = Article(url)
    article.html = html_content
    article.parse()
    
    try:
        article.nlp()
        summary = article.summary
        keywords = article.keywords
    except Exception:
        summary = "Summary extraction failed"
        keywords = []
    
    return {
        "title": article.title,
        "text": article.text,
        "summary": summary,
        "keywords": keywords,
        "publish_date": article.publish_date
    }

def extract_article_content_with_trafilatura(html_content):
    """
    Extracts the main article content from HTML using trafilatura.
    """
    return trafilatura.extract(html_content, include_comments=False, include_tables=False, no_fallback=True)

def get_page_content(url, headless=True):
    """
    Fetches and returns relevant article content from a webpage using Playwright.
    
    :param url: The URL of the page to fetch.
    :param headless: Whether to run in headless mode (default is True).
    :return: Dictionary containing article information.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        
        page.set_viewport_size({"width": 1366, "height": 768})
        
        page.goto(url, timeout=60000)
        
        page.wait_for_load_state("networkidle")
        
        html_content = page.content()
        
        browser.close()
        
        return html_content

def get_articles_from_source(source_url, max_articles=5, headless=True):
    source = newspaper.build(source_url, memoize_articles=False)
    
    article_urls = [article.url for article in source.articles[:max_articles]]
    
    articles = []
    for url in article_urls:
        try:
            html_content = get_page_content(url, headless)
            article_content = extract_article_content_with_newspaper(html_content, url)
            articles.append(article_content)
            time.sleep(random.uniform(1, 3))
        except Exception as e:
            print(f"Error processing {url}: {e}")
    
    return articles
