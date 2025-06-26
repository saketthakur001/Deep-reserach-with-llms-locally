import keyring
from google import genai
from transformers import AutoTokenizer, PegasusForConditionalGeneration
from LLM import llm

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
        return "Error: GEMINI_API_KEY environment variable not set."

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemma-3-12b-it')

    prompt = f"Please provide a concise summary of the following text:\n\n{text}"

    response = model.generate_content(prompt)

    if response and response.text:
      return response.text
    else:
      return "Error: Could not generate summary. Response might be empty or filtered."

  except Exception as e:
    return f"An error occurred: {e}"

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
