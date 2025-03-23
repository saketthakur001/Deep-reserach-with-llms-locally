# using quantized models with llama_cpp
from llama_cpp import Llama

#load the quantized model from hugging face
#make sure the model file is in the same directory or provide the full path
llm = Llama.from_pretrained(
    repo_id="unsloth/gemma-3-1b-it-GGUF",
    filename="gemma-3-1b-it-Q5_K_M.gguf",
)

def summarize_paragraph(paragraph: str) -> str:
    #generate a summary for the given paragraph
    prompt = f"Summarize the following text concisely:\n\n{paragraph}\n\nSummary:"
    
    response = llm.create_chat_completion(
        messages=[{"role": "user", "content": prompt}]
    )
    
    #extract and return the generated summary
    return response["choices"][0]["message"]["content"].strip()

def enhance_query(query, num_variations=3):
    """
    generate multiple enhanced versions of a given search query.
    helps improve search relevance by rewording the query in different ways.
    
    :param query: the original search phrase.
    :param num_variations: how many variations to generate (between 1 and 10).
    :return: list of alternative search queries.
    """
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

#example usage
query = "future of AI in healthcare"
enhanced_queries = enhance_query(query, 5)

print("Original Query:", query)
print("Enhanced Queries:")
for idx, q in enumerate(enhanced_queries, start=1):
    print(f"{idx}. {q}")

#standard python entry point
if __name__ == "__main__":
    text = """  """  #add text to summarize here
    print(summarize_paragraph(text))
