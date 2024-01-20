from openai import OpenAI
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

status = client.fine_tuning.jobs.retrieve("job-urhktM573AjTiLbDtzJTO62r")