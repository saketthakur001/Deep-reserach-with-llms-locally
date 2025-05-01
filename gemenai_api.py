#pip install google-genai
#pip install keyring

import keyring
from google import genai

# after adding the key you remove this part, the key will be added to your env.
#keyring.set_password("gemini_key", 'user1', "the key")

retrieved_key = keyring.get_password("gemini_key", "user1")

client = genai.Client(api_key=retrieved_key)

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Explain how AI works in a few words",
)

print(response.text)
