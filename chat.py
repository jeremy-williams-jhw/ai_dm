from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI API key
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))



# Chat function to interact with ChatGPT
def chat_with_gpt(messages, model="gpt-3.5-turbo"):
    """
    Send a list of messages to OpenAI's API and receive a response.
    :param messages: List of messages in OpenAI's chat format.
    :param model: OpenAI model to use (default: gpt-4).
    :return: The response from the API.
    """
    
    try:
        response = client.chat.completions.create(
            model=model,  # Specify the model to use
            # messages=[message.dict() for message in messages]
            messages=messages
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"An error occurred: {e}"