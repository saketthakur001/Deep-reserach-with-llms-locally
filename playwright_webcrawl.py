from playwright.sync_api import sync_playwright
import random
import time


def get_page_text(url, headless=True):
    """
    Fetches and returns all visible text from a webpage using Playwright.
    
    :param url: The URL of the page to fetch.
    :param headless: Whether to run in headless mode (default is True).
    :return: The text content of the page.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        page.goto(url, timeout=60000)
        page_text = page.inner_text("body")  # Extract all visible text
        browser.close()
        return page_text


# Fix the stealth mode issue
# from playwright_stealth import stealth

# def get_page_text(url, headless=True, proxy=None):
#     """
#     Fetches and returns all visible text from a webpage using Playwright in stealth mode.

#     :param url: The URL of the page to fetch.
#     :param headless: Whether to run in headless mode (default is True).
#     :param proxy: Optional proxy (format: "http://user:pass@proxy_ip:port")
#     :return: The text content of the page.
#     """
#     with sync_playwright() as p:
#         browser_args = {"headless": headless}
#         if proxy:
#             browser_args["proxy"] = {"server": proxy}

#         browser = p.chromium.launch(**browser_args)
#         context = browser.new_context(
#             user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)",  # Fake browser
#             viewport={"width": random.randint(800, 1920), "height": random.randint(600, 1080)}
#         )

#         page = context.new_page()
#         stealth(page)  # Enable stealth mode
          
#         try:
#             page.goto(url, timeout=60000, wait_until="domcontentloaded")
#             time.sleep(random.uniform(2, 5))  # Mimic human browsing behavior
#             page_text = page.inner_text("body")
#         except Exception as e:
#             print(f"Error loading {url}: {e}")
#             page_text = None

#         browser.close()
#         return page_text

# Example usage:
# text = get_page_text("https://example.com", proxy="http://user:pass@proxy_ip:port")
# print(text)

if __name__ == "__main__":
    # test
    url = "https://en.wikipedia.org/wiki/Meaning_of_life#Questions"
    # print(get_page_text(url, headless=False))  # Run in normal mode
    print(get_page_text(url, headless=True))   # Run in headless mode
