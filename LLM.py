# using quantized models with llama_cpp
import json
from llama_cpp import Llama

#quantized model from hugging face
# make sure the model file is in the same directory or provide the full path context widnow max
llm = Llama.from_pretrained(
    repo_id="unsloth/gemma-3-1b-it-GGUF",
    filename="gemma-3-1b-it-Q5_K_M.gguf",
    n_ctx=20000
    )


import re

def truncate_text_by_words(text, word_limit):
    words = text.split()
    print(len(words))
    word_limit-=1
    if len(words) <= word_limit:
        return text #if text is alreay in light than return it

    truncated_words = words[:word_limit]

    #serach for the next sentese
    remaining_text = " ".join(words[word_limit:])
    sentence_end = re.search(r"[.!?]", remaining_text)

    if sentence_end:
        end_index = sentence_end.end()  #include the full sentense 
        truncated_text = " ".join(truncated_words) + " " + remaining_text[:end_index]
    else:
        truncated_text = " ".join(truncated_words)  #if no sentese end.

    return truncated_text.strip()



def summarize_paragraph(paragraph: str) -> str:
    #generate a summary for the given paragraph
    prompt = f"Summarize the following text concisely:\n\n{paragraph}\n\n compressed version:"
    
    response = llm.create_chat_completion(messages=[{"role": "user", "content": prompt}])
    
    print('numb bals'*100)
    # print(response["choices"][0]["message"]["content"].strip())
    return response["choices"][0]["message"]["content"].strip()


def enhance_query_into_two(query: str) -> list:
    prompt = (
        f"Rewrite the following search query into multiple improved versions. "
        f"If the query is complex, break it into two or multiple separate queries that capture its different aspects.\n\n"
        f"Query: {query}\n\n"
        f"Provide all variations, each on a new line."
        f"example:- this is an example query"
    )
    
    response = llm.create_chat_completion(messages=[{"role": "user", "content": prompt}])
    #The response might include bullet points or other formatting, so we do a basic cleanup:
    queries = response["choices"][0]["message"]["content"].strip().split("\n")[2:]
    return [q.strip("- ").strip("* ").strip() for q in queries if q.strip()]



#standard python entry point
if __name__ == "__main__":
    text = """ testinng fomr text"""
    # print(summarize_paragraph(text))

    #testinng enhanced query
    print(enhance_query_into_two('why do cats don\'t spill their milk?'))

    
    #example usage
    # query = "future of AI in healthcare"
    # enhanced_queries = enhance_query(query, 5)

    # print("Original Query:", query)
    # print("Enhanced Queries:")
    # for idx, q in enumerate(enhanced_queries, start=1):
    #     print(f"{idx}. {q}")

