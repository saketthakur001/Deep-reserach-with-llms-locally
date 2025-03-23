import trafilatura

def extract_article(html_file):
    with open(html_file, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # Extract main content
    extracted_text = trafilatura.extract(html_content)
    
    if extracted_text:
        return extracted_text
    else:
        return "Failed to extract main content."

# Example usage
html_file = 'html_content.html'
article_text = extract_article(html_file)

print(article_text)  # Or save it to a file
