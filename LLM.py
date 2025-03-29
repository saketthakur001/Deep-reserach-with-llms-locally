# using quantized models with llama_cpp
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


def enhance_query(query, num_variations=3):
    num_variations = max(1, min(num_variations, 10))  #keep within valid range

    prompt = (
        f"rewrite the following search query in {num_variations} different ways to improve accuracy:\n\n"
        f"Query: {query}\n\n"
        f"Provide {num_variations} variations, each on a new line."
    )
    
    output = llm(prompt, max_tokens=200)
    
    #extract and clean up the generated query variations
    queries = output["choices"][0]["text"].strip().split("\n")
    return [q.strip("- ").strip() for q in queries if q.strip()]

def enhance_query_into_two(query: str) -> list:
    """
    Enhance a search query by rewriting it into two variations.
    If the query is complex, break it into two simpler queries.
    """
    prompt = (
        f"Rewrite the following search query into multiple improved versions. "
        f"If the query is complex, break it into two or multiple separate queries that capture its different aspects.\n\n"
        f"Query: {query}\n\n"
        f"Provide all variations, each on a new line."
    )
    
    response = llm.create_chat_completion(messages=[{"role": "user", "content": prompt}])
    #The response might include bullet points or other formatting, so we do a basic cleanup:
    queries = response["choices"][0]["message"]["content"].strip().split("\n")
    return [q.strip("- ").strip() for q in queries if q.strip()]

# if __name__ == "__main__":
#     original_query = "How does AI impact modern healthcare policies and what future trends should we expect?"
#     variations = enhance_query_into_two(original_query)
#     print("Enhanced Queries:")
#     for idx, q in enumerate(variations, start=1):
#         print(f"{idx}. {q}")


# print(__name__)

#standard python entry point
if __name__ == "__main__":
    text = """ testinng fomr text"""
    # print(summarize_paragraph(text))

    #testinng enhanced query
    print(enhance_query_into_two('what is the meaning of life?'))


    #example usage
    # query = "future of AI in healthcare"
    # enhanced_queries = enhance_query(query, 5)

    # print("Original Query:", query)
    # print("Enhanced Queries:")
    # for idx, q in enumerate(enhanced_queries, start=1):
    #     print(f"{idx}. {q}")

