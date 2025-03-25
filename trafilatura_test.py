import trafilatura

def extract_clean_article(html_file, include_comments=False, include_tables=False, no_fallback=True):
    with open(html_file, "r", encoding="utf-8") as f:
        html_content = f.read()

    #extract only the main article with the given parameters
    extracted_text = trafilatura.extract(
        html_content,
        include_comments=include_comments,
        include_tables=include_tables,
        no_fallback=no_fallback
    )
    return extracted_text.strip() if extracted_text else "Failed to extract main article."

#print(__name__)
if __name__ == "__main__":
    html_file = "html_content.html" # test an html file here  
    article_text = extract_clean_article(html_file)
    # save the article to a file
    with open("article_text.txt", "w", encoding="utf-8") as f:
        f.write(article_text)
    print(article_text) 
