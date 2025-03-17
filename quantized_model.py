from llama_cpp import Llama

# Load your model (you can use from_pretrained to pull it from Hugging Face)
llm = Llama.from_pretrained(
    repo_id="unsloth/gemma-3-1b-it-GGUF",
    filename="gemma-3-1b-it-Q5_K_M.gguf",
)

def summarize_paragraph(paragraph: str) -> str:
    # Craft a prompt that instructs the model to summarize
    prompt = f"Summarize the following text concisely:\n\n{paragraph}\n\nSummary:"
    response = llm.create_chat_completion(
        messages=[{"role": "user", "content": prompt}]
    )
    # Extract the summary from the response
    summary = response["choices"][0]["message"]["content"].strip()
    return summary

# Example usage:
text = (
    """saket's age is 20, he is a student. He is studying in college. He is a good student
    and he is very intelligent. He is very good at studies. He is very good at sports. He is very good at
    playing cricket. He is very good at playing football. He is very good at playing basketball. He is very good at
    playing volleyball. He is very good at playing badminton. He is very good at playing tennis. He is very good at
    playing table tennis. He is very good at playing chess. He is very good at playing carrom. He is very good at
    playing ludo. He is very good at playing snake and ladder. He is very good at playing video games. He is very good at
    playing computer games. He is very good at playing mobile games. He is very good at playing online games. He is very good at
    playing offline games. He is very good at playing indoor games. He is very good at playing outdoor games."""
)

print(summarize_paragraph(text))