from openai import OpenAI
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

client.files.create(file=open("history/training_data_small.jsonl", "rb"), purpose="fine-tune")
