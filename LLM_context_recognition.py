from huggingface_hub import hf_hub_download

model_path = hf_hub_download(
    repo_id="DeepSeek/DeepSeek-R1-8B-GGUF",
    filename="deepseek-r1-8b.Q4_K_M.gguf",
    local_dir="./models"
)
