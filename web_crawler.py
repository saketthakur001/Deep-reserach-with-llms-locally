from playwright.async_api import async_playwright
import random
import asyncio
import time
from newspaper import Article
import newspaper
import trafilatura
import keyring

# List of common user agents to rotate
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
    "Mozilla/5.0 (X11; CrOS armv7l 13597.84.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; AS; rv:11.0) like Gecko"
]

# Placeholder for proxy configuration
# PROXIES = [
#     "http://user:pass@proxy.example.com:8080",
#     "http://user:pass@another.proxy.com:8080",
# ]

async def extract_article_content_with_newspaper(html_content, url):
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

async def extract_article_content_with_trafilatura(html_content):
    """
    Extracts the main article content from HTML using trafilatura.
    """
    return trafilatura.extract(html_content, include_comments=False, include_tables=False, no_fallback=True)

async def get_page_content(url, headless=True, retries=3, delay_multiplier=2):
    """
    Fetches and returns relevant article content from a webpage using Playwright.
    Includes retry logic with exponential backoff and random delays.
    
    :param url: The URL of the page to fetch.
    :param headless: Whether to run in headless mode (default is True).
    :param retries: Number of retries for fetching the page.
    :param delay_multiplier: Multiplier for exponential backoff delay.
    :return: Dictionary containing article information.
    """
    for attempt in range(retries):
        try:
            async with async_playwright() as p:
                # proxy = random.choice(PROXIES) if PROXIES else None
                browser = await p.chromium.launch(headless=headless) # , proxy={"server": proxy} if proxy else {})
                user_agent = random.choice(USER_AGENTS)
                page = await browser.new_page(user_agent=user_agent)
                
                await page.set_viewport_size({"width": 1366, "height": 768})
                
                await page.goto(url, timeout=60000)
                
                # More robust waiting for content to load
                await page.wait_for_load_state("networkidle")
                await asyncio.sleep(random.uniform(1, 3)) # Dynamic delay
                
                html_content = await page.content()
                
                await browser.close()
                
                return html_content
        except Exception as e:
            print(f"Attempt {attempt + 1} failed for {url}: {e}")
            if attempt < retries - 1:
                delay = random.uniform(delay_multiplier ** attempt, delay_multiplier ** (attempt + 1))
                print(f"Retrying {url} in {delay:.2f} seconds...")
                await asyncio.sleep(delay)
            else:
                print(f"Failed to fetch {url} after {retries} attempts.")
                return None

async def get_all_text_from_page(url, headless=True, retries=3, delay_multiplier=2):
    """
    Fetches and returns all visible text content from a webpage using Playwright.
    Includes retry logic with exponential backoff and random delays.
    
    :param url: The URL of the page to fetch.
    :param headless: Whether to run in headless mode (default is True).
    :param retries: Number of retries for fetching the page.
    :param delay_multiplier: Multiplier for exponential backoff delay.
    :return: A string containing all visible text from the page.
    """
    for attempt in range(retries):
        try:
            async with async_playwright() as p:
                # proxy = random.choice(PROXIES) if PROXIES else None
                browser = await p.chromium.launch(headless=headless) # , proxy={"server": proxy} if proxy else {})
                user_agent = random.choice(USER_AGENTS)
                page = await browser.new_page(user_agent=user_agent)
                
                await page.set_viewport_size({"width": 1366, "height": 768})
                
                await page.goto(url, timeout=60000)
                
                await page.wait_for_load_state("networkidle")
                await asyncio.sleep(random.uniform(1, 3)) # Dynamic delay
                
                all_text = await page.locator('body').all_text_contents()
                
                await browser.close()
                
                return "\n".join(all_text).strip()
        except Exception as e:
            print(f"Attempt {attempt + 1} failed for {url}: {e}")
            if attempt < retries - 1:
                delay = random.uniform(delay_multiplier ** attempt, delay_multiplier ** (attempt + 1))
                print(f"Retrying {url} in {delay:.2f} seconds...")
                await asyncio.sleep(delay)
            else:
                print(f"Failed to fetch {url} after {retries} attempts.")
                return None

async def get_articles_from_source(source_url, max_articles=5, headless=True):
    source = newspaper.build(source_url, memoize_articles=False)
    
    article_urls = [article.url for article in source.articles[:max_articles]]
    
    articles = []
    for url in article_urls:
        try:
            html_content = await get_page_content(url, headless)
            if html_content:
                article_content = await extract_article_content_with_newspaper(html_content, url)
                articles.append(article_content)
            await asyncio.sleep(random.uniform(1, 3)) # Be polite
        except Exception as e:
            print(f"Error processing {url}: {e}")
    
    return articles