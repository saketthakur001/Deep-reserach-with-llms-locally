# Local Deep Research with LLMs

## Project Overview

This project aims to create a powerful, local alternative to services like Perplexity AI. The core idea is to perform deep, automated research on a given topic by:

1.  **Enhancing and expanding** a user's initial query.
2.  **Searching the web** for relevant information using the expanded queries.
3.  **Crawling and extracting** the content from the search results.
4.  **Summarizing and synthesizing** the extracted information using a local Large Language Model (LLM).
5.  **Presenting the user with a comprehensive and well-structured report.**

The project is in its early stages, with several key components already implemented, but not yet integrated.

## Current State

The project is currently a collection of Python scripts, each responsible for a specific part of the research pipeline. Here's a breakdown of the existing components:

*   **`main.py`**: The intended entry point for the application, but currently empty.
*   **`LLM.py`**:  Handles interactions with a local, quantized LLM (Gemma 3.1B). It includes functions for summarizing text and enhancing user queries.
*   **`google_search_api.py`**:  Performs Google searches using the Custom Search JSON API.
*   **`playwright_webcrawl.py`**:  Uses Playwright and the `newspaper4k` library to crawl web pages and extract article content.
*   **`gemenai_api.py`**: Interacts with the Google Gemini API for text summarization.
*   **`pegasus_text_summarization.py`**:  Uses the Pegasus model for text summarization.
*   **`trafilatura_test.py`**:  A script for testing the `trafilatura` library for web content extraction.
*   **`LLM_context_recognition.py`**:  Another script that uses the Pegasus model for summarization.
*   **`non-quantized_version.py`**: A script for using a non-quantized Gemma model.

## Recommendations for Improvement

The current codebase is a great starting point, but it can be significantly improved in terms of structure, efficiency, and maintainability. Here are some recommendations:

### 1.  **Code Structure and Organization**

*   **Create a unified entry point:** The `main.py` file should be the single entry point for the application. It should orchestrate the entire research process, calling functions from the other modules.
*   **Consolidate functionality:** You have multiple scripts for summarization (`gemenai_api.py`, `pegasus_text_summarization.py`, `LLM_context_recognition.py`). You should choose one primary summarization method and consolidate that logic into a single module (e.g., `summarizer.py`). You can keep the others as experimental alternatives, but they shouldn't be part of the main workflow.
*   **Create a dedicated `web_crawler` module:** The functionality in `playwright_webcrawl.py` and `trafilatura_test.py` should be combined into a single `web_crawler.py` module that handles all web content extraction.
*   **Use a configuration file:** Instead of hardcoding API keys and other settings in your scripts, use a configuration file (e.g., `config.ini` or `config.yaml`) to store these values. This makes it easier to manage and change your settings without modifying the code.
*   **Create a `requirements.txt` file:** You have an `Installation` section in your README that mentions a `requirements.txt` file, but the file doesn't exist. You should create one to list all the project's dependencies.

### 2.  **Code Quality and Best Practices**

*   **Error handling:** The scripts lack robust error handling. For example, what happens if a web page fails to load, or an API call fails? You should add `try...except` blocks to handle these situations gracefully.
*   **Logging:** Instead of using `print()` statements for debugging, use the `logging` module. This will allow you to control the level of logging and write logs to a file.
*   **Docstrings and comments:** While you have some docstrings, they could be more detailed. Explain what each function does, its parameters, and what it returns. Add comments to explain complex parts of your code.
*   **Consistent naming conventions:** Use consistent naming conventions for your variables, functions, and modules. For example, use `snake_case` for function and variable names.
*   **Remove unused code:** There's a significant amount of commented-out code in `playwright_webcrawl.py`. This should be removed to improve readability.

### 3.  **Functionality and Features**

*   **Integrate the components:** The biggest missing piece is the integration of all the different components. The `main.py` file should be the glue that holds everything together.
*   **Implement the core workflow:** The core research workflow (query enhancement -> search -> crawl -> summarize) needs to be implemented in `main.py`.
*   **Add a user interface:** Currently, the project is a collection of scripts. To make it more user-friendly, you could create a simple command-line interface (CLI) using a library like `argparse` or `click`, or even a web interface using a framework like Flask or FastAPI.
*   **Improve the summarization:** You're using a few different summarization techniques. You should experiment with them to see which one gives you the best results. You could also try to implement a more advanced summarization technique, such as a multi-document summarization model.

### 4.  **What you have done wrong (and how to fix it)**

*   **Scattered and redundant code:** You have multiple files doing similar things (e.g., summarization). This makes the code hard to maintain. **Fix:** Consolidate the redundant code into a single module.
*   **Lack of a central orchestrator:** There's no single script that runs the entire research process. **Fix:** Implement the core logic in `main.py`.
*   **Hardcoded secrets:** Your API keys are hardcoded in the scripts. This is a security risk. **Fix:** Use a configuration file or environment variables to store your API keys.
*   **No dependency management:** There's no `requirements.txt` file, which makes it hard for others to set up the project. **Fix:** Create a `requirements.txt` file.

By addressing these points, you can transform your project from a collection of scripts into a robust and powerful research tool.