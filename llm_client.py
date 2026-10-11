
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise RuntimeError(
        "GROQ_API_KEY is missing. Check your .env file."
    )

# Initialize the Groq client
llm = Groq(api_key=api_key)

# Model served through Groq
MODEL = "openai/gpt-oss-20b"


def generate_response(prompt: str) -> str:
    """Send a prompt to the LLM and return its answer as a string."""

    if not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    response = llm.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_completion_tokens=500
    )

    # Extract the generated answer
    answer = response.choices[0].message.content

    if not answer or not answer.strip():
        raise RuntimeError(
            "The model returned an empty response."
        )

    return answer.strip()
