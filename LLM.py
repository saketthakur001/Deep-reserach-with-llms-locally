# using quantized models with llama_cpp
from llama_cpp import Llama

#load the quantized model from hugging face
#make sure the model file is in the same directory or provide the full path context widnow max
llm = Llama.from_pretrained(
    repo_id="unsloth/gemma-3-1b-it-GGUF",
    filename="gemma-3-1b-it-Q5_K_M.gguf",
    n_ctx=20000
    )

def summarize_paragraph(paragraph: str) -> str:
    #generate a summary for the given paragraph
    prompt = f"Summarize the following text concisely:\n\n{paragraph}\n\nSummary:"
    
    response = llm.create_chat_completion(
        messages=[{"role": "user", "content": prompt}])
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
# print(__name__)

#standard python entry point
if __name__ == "__main__":
    text = """ testinng fomr text"""
    print(summarize_paragraph(text))


    #example usage
    # query = "future of AI in healthcare"
    # enhanced_queries = enhance_query(query, 5)

    # print("Original Query:", query)
    # print("Enhanced Queries:")
    # for idx, q in enumerate(enhanced_queries, start=1):
    #     print(f"{idx}. {q}")
