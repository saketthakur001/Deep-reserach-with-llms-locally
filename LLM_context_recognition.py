from transformers import pipeline 


model_id = "google/gemma-3-1b-it"
summarizer = pipeline("summarization", model=model_id, device=0, torch_dtype="bfloat16")


text = """
The lms command is part of LM Studio's CLI tool and needs to be set up properly before use. Here's how you can install and configure it:
Steps to Install and Set Up lms CLI

    Install LM Studio:

        Download LM Studio from its official website or repository, depending on your operating system (Linux, macOS, or Windows)

    .

Run LM Studio Once:

    Before using lms, you must launch LM Studio at least once to initialize its working directory

    .

Bootstrap lms:

    For Linux/macOS:

bash
~/.lmstudio/bin/lms bootstrap

For Windows (PowerShell):

powershell
cmd /c %USERPROFILE%/.lmstudio/bin/lms.exe bootstrap

Ensure the path to the lms executable matches your installation directory

    .

Verify Installation:

    Open a new terminal window and run:

bash
lms --version

This should display the version of the CLI tool

    .

Use the Command:

    Once installed, you can use commands like:

        bash
        lms get gemma-3-1b

If the lms command is still not recognized, ensure that LM Studio is installed correctly and its binaries are added to your system's PATH variable
.
"""

prompt = f"Summarize the following text \n\n{text}\n\n Summary:"
summarizer(prompt, max_new_tokens=150, do_sample=False)
print("Generated Summary: ", summarizer)

