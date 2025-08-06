import keyring
from transformers import AutoTokenizer, PegasusForConditionalGeneration
from LLM import llm
import logging
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# def summarize_with_gemini(text: str) -> str:
#     """
#     Generate a summary for the given text using the Gemini API.
#     Falls back to local LLM if Gemini is unavailable or fails.

#     Args:
#         text: The input text to be summarized.

#     Returns:
#         A summary string, or error message if both methods fail.
#     """
#     try:
#         api_key = keyring.get_password("gemini_key", "user1")
#         if not api_key:
#             logging.warning("GEMINI_API_KEY not found in keyring. Falling back to local LLM.")
#             return summarize_with_local_llm(text)

#         model = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=api_key)

#         prompt = f"Please provide a concise summary of the following text:\n\n{text}"
#         response = model.invoke([HumanMessage(content=prompt)])

#         if response and response.content:
#             logging.info("Using Gemini for summarization.")
#             return response.content
#         else:
#             logging.warning("Gemini returned empty or invalid response. Falling back to local LLM.")
#             return summarize_with_local_llm(text)

#     except Exception:
#         logging.exception("An error occurred during Gemini summarization. Falling back to local LLM.")
#         return summarize_with_local_llm(text)



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