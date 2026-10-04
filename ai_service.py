import os

from dotenv import load_dotenv
from huggingface_hub import InferenceClient


# Load variables from the .env file
load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")


def ask_gemma(message):

    if not HF_TOKEN:
        return "Error: HF_TOKEN was not found."

    try:

        client = InferenceClient(
            provider="auto",
            api_key=HF_TOKEN
        )

        response = client.chat.completions.create(
            model="google/gemma-3-4b-it",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are PantryPal, a friendly "
                        "AI kitchen assistant."
                    )
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            max_tokens=300
        )

        return response.choices[0].message.content

    except Exception as error:

        return f"AI Error: {error}"


# Temporary test
if __name__ == "__main__":

    answer = ask_gemma(
        "Say hello and tell me one simple dish "
        "I can make using eggs and tomatoes."
    )

    print(answer)