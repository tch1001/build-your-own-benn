from openai import OpenAI
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

client.fine_tuning.jobs.create(
    training_file="file-bWGv8gFrS8JledRgdcxQBOe0",
    model="gpt-3.5-turbo-0613",
    hyperparameters={
        "n_epochs": 1,
    }
) 