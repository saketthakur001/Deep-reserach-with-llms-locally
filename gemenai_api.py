#pip install google-genai
#pip install keyring

import keyring
from google import genai

# after adding the key you remove this part, the key will be added to your env.
#keyring.set_password("gemini_key", 'user1', "the key")

api_key = keyring.get_password("gemini_key", "user1")

# client = genai.Client(api_key=retrieved_key)

# response = client.models.generate_content(
#     model="gemini-2.0-flash",
#     contents="Explain how AI works in a few words",
# )

# print(response.text)


import os
import google.generativeai as genai

def summarize_text(text: str) -> str:
  """
  Generates a summary for the given text using the Gemini API.

  Args:
    text: The input text to be summarized.

  Returns:
    A string containing the summary of the text.
    Returns an error message if summarization fails.
  """
  try:
    # Ensure your API key is securely stored and accessed.
    # For this example, we assume it's in an environment variable.
    # Replace with your preferred method of handling API keys.
    # api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "Error: GEMINI_API_KEY environment variable not set."

    genai.configure(api_key=api_key)

    # Use a model suitable for text generation/summarization
    # "gemini-1.5-flash" or "gemini-1.0-pro" are good choices
    # "gemini-2.0-flash" is not a standard model name, assuming
    # it might be a typo or internal name. Using a standard one.
    model = genai.GenerativeModel('gemma-3-12b-it')

    prompt = f"Please provide a concise summary of the following text:\n\n{text}"

    response = model.generate_content(prompt)

    # Check if the response has text content
    if response and response.text:
      return response.text
    else:
      # Handle cases where the model might not return text (e.g., safety filters)
      return "Error: Could not generate summary. Response might be empty or filtered."

  except Exception as e:
    return f"An error occurred: {e}"

# Example usage:
if __name__ == "__main__":
  sample_text = """
  Artificial intelligence (AI) is a broad field of computer science
  concerned with building smart machines capable of performing tasks that
  typically require human intelligence. AI can be categorized into two main
  types: narrow or weak AI, which is designed and trained for a particular
  task, and general or strong AI, which is a theoretical type of AI that
  can perform any intellectual task that a human being can. Machine learning
  is a subset of AI that focuses on the development of systems that can
  learn from data. Deep learning is a further subset of machine learning
  that uses neural networks with multiple layers (deep neural networks) to
  analyze various factors with more weight than others, in a manner similar
  to how the human brain works.
  """

  summary = summarize_text(sample_text)
  print("Original Text:")
  print(sample_text)
  print("\nSummary:")
  print(summary)