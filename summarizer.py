import keyring
from google import genai
from transformers import AutoTokenizer, PegasusForConditionalGeneration
from LLM import llm
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def summarize_with_gemini(text: str) -> str:
  """
  Generates a summary for the given text using the Gemini API.

  Args:
    text: The input text to be summarized.

  Returns:
    A string containing the summary of the text.
    Returns an error message if summarization fails.
  """
  try:
    api_key = keyring.get_password("gemini_key", "user1")
    if not api_key:
        logging.warning("GEMINI_API_KEY not found in keyring. Falling back to local LLM for summarization.")
        return summarize_with_local_llm(text)

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemma-3-12b-it') # Using gemma-3-12b-it as requested

    prompt = f"Please provide a concise summary of the following text:\n\n{text}"

    response = model.generate_content(prompt)

    if response and response.text:
      logging.info("Using Gemini for summarization.")
      return response.text
    else:
      logging.warning("Gemini summarization failed or returned empty response. Falling back to local LLM.")
      return summarize_with_local_llm(text)

  except Exception as e:
    logging.error(f"An error occurred during Gemini summarization: {e}. Falling back to local LLM.")
    return summarize_with_local_llm(text)

def summarize_with_pegasus(text: str) -> str:
    """
    Summarizes the given text using the Pegasus model.

    Args:
        text: The input text to be summarized.

    Returns:
        A string containing the summary of the text.
    """
    model = PegasusForConditionalGeneration.from_pretrained("google/pegasus-xsum")
    tokenizer = AutoTokenizer.from_pretrained("google/pegasus-xsum")
    inputs = tokenizer(text, max_length=1024, return_tensors="pt", truncation=True)
    summary_ids = model.generate(inputs["input_ids"])
    summary = tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True)[0]
    return summary

def summarize_with_local_llm(paragraph: str) -> str:
    """
    Summarizes a paragraph using the local LLM.

    Args:
        paragraph: The paragraph to summarize.

    Returns:
        The summarized paragraph.
    """
    prompt = f"Summarize the following text concisely:\n\n{paragraph}\n\n compressed version:"
    
    response = llm.create_chat_completion(messages=[{"role": "user", "content": prompt}])
    
    return response["choices"][0]["message"]["content"].strip()