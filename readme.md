# Local Deep Research with LLMs

## Project Overview

This project aims to create a powerful, local alternative to services like Perplexity AI. The core idea is to perform deep, automated research on a given topic by:

1.  **Enhancing and expanding** a user's initial query.
2.  **Searching the web** for relevant information using the expanded queries.
3.  **Crawling and extracting** the content from the search results.
4.  **Summarizing and synthesizing** the extracted information using a local Large Language Model (LLM).
5.  **Presenting the user with a comprehensive and well-structured report.**

The project is in its early stages, with several key components already implemented and integrated within `main.py`.

## Current State

The project is currently a collection of Python scripts, each responsible for a specific part of the research pipeline. Here's a breakdown of the existing components:

*   **`main.py`**: The central entry point for the application. It orchestrates the entire research process, calling functions from other modules to perform query enhancement, web search, content crawling, and summarization.
*   **`LLM.py`**: Handles interactions with LLMs for query enhancement and classification. It defaults to using the Gemini API (`gemma-3-12b-it`) and falls back to a local, quantized LLM (Gemma 3.1B) if the Gemini API is unavailable or encounters an error.
*   **`google_search_api.py`**: Performs Google searches using the Custom Search JSON API. API keys are securely managed using `keyring`.
*   **`web_crawler.py`**: Uses Playwright, `newspaper4k`, and `trafilatura` to crawl web pages and extract article content.
*   **`summarizer.py`**: Contains functions for text summarization, including methods using the Gemini API (`gemma-3-12b-it`), a local LLM, and the Pegasus model. `main.py` now defaults to using the Gemini API for summarization, with a fallback to the local LLM.
*   **`person_researcher.py`**: Dedicated module for researching information about specific individuals.
*   **`utils.py`**: Contains utility functions, such as text truncation.
*   **`requirements.txt`**: Lists all project dependencies for easy installation.

## Recommendations for Improvement

The current codebase is a great starting point, and significant progress has been made in integrating components. Here are some recommendations for further improvement in terms of structure, efficiency, and maintainability:

### 1.  **Code Quality and Best Practices**

*   **Error handling:** The scripts could benefit from more robust error handling. For example, what happens if a web page fails to load, or an API call fails? You should add `try...except` blocks to handle these situations gracefully.
*   **Logging:** Instead of using `print()` statements for debugging, use the `logging` module. This will allow you to control the level of logging and write logs to a file.
*   **Docstrings and comments:** While some docstrings exist, they could be more detailed. Explain what each function does, its parameters, and what it returns. Add comments to explain complex parts of your code.
*   **Consistent naming conventions:** Use consistent naming conventions for your variables, functions, and modules. For example, use `snake_case` for function and variable names.
*   **Remove unused code:** Ensure there is no significant amount of commented-out or unused code that could hinder readability.

### 2.  **Functionality and Features**

*   **Add a user interface:** Currently, the project is primarily a collection of scripts. To make it more user-friendly, you could create a simple command-line interface (CLI) using a library like `argparse` or `click`, or even a web interface using a framework like Flask or FastAPI.
*   **Improve the summarization:** Experiment with the different summarization techniques available in `summarizer.py` to determine which one yields the best results for your use case. You could also explore implementing more advanced summarization techniques, such as multi-document summarization models.
*   **Refine `person_researcher.py`**: Further develop the `person_researcher.py` module to provide more in-depth and structured information for person-specific queries.

By addressing these points, you can transform your project into an even more robust and powerful research tool.
