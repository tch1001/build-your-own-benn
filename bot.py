import random
from dotenv import load_dotenv
load_dotenv()

import logging
from telegram import Update, InputFile
from telegram.ext import Updater, CommandHandler, CallbackContext, Application, MessageHandler, CallbackContext
import os
import pickle
import face_recognition as fr

from io import BytesIO
from openai import OpenAI
import requests

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

logger = logging.getLogger(__name__)

with open("history/catchphrases.txt", "r") as f:
    catchphrases = f.readlines()
    for i in range(len(catchphrases)):
        catchphrases[i] = catchphrases[i].strip()
catchphrases = '\n'.join(catchphrases)

preamble = "You are Benn Tan. You are a NUS university computer science student who wants to get into jane street. You act like a Singaporean 60 year old uncle. tch refers to your friend, NOT a sound of disapproval."

prompt = {"role": "system", "content": preamble + "reply messages like a singaporean texting style, with all lower case, MAKE SURE IT'S BELOW 5 sentences. be sure to use the following catchphrases" + catchphrases}


model = 'gpt-3.5-turbo-0613'

def checkIsBenn(filename):
    image = fr.load_image_file(filename)
    faceLoc = fr.face_locations(image)#,model='cnn')
    faceEncodings = fr.face_encodings(image,faceLoc)

    for encoding in faceEncodings:
        vecDist = fr.face_distance(sampleData,encoding)
        vecDist.sort()
        extremeLimit = vecDist.shape[0]//10

        vecDist2 = vecDist[extremeLimit:-extremeLimit] #remove top and bottom 10%: noisy

        if vecDist2.mean()<0.55:
            return True

    return False

async def reply(update: Update, context: CallbackContext) -> None:
    print(update.message)
    if update.message.photo:
        # Download
        photo_file_path = f"temp/{update.message.chat_id}.jpg"
        photo_file = await context.bot.get_file(update.message.photo[-1].file_id)
        # download the jpg from this url photo_file.file_path using python requests
        file = requests.get(photo_file.file_path)
        # save the file to the path photo_file_path
        open(photo_file_path, 'wb').write(file.content)

        # Check if the photo contains Benn Tan's face
        is_benn = checkIsBenn(photo_file_path)

        # Send the result back to the user
        positive_responses = [
            "eh stalker",
            "why you got my photo",
            "stop stalking me",
            "this guy hot sia"
        ]
        negative_responses = [
            "who tf is that",
            "who is this, that's not me",
            "why you send me random picture",
        ]
        if(is_benn):
            response = random.choice(positive_responses)
        else:
            response = random.choice(negative_responses)

        await update.message.reply_text(response)

        # Clean up temporary photo file
        os.remove(photo_file_path)
    else:
        completion = client.chat.completions.create(
            model = model,
            messages=[
                prompt,
                {"role": "user", "content": update.message.text} 
            ],
        )
        response = completion.choices[0].message.content
        if response == "":
            response = 'huh'
        if '```' in response:
            splitted_response = response.split('```')
            response = splitted_response[0]
            code = '\n'.join(splitted_response[1].split('\n')[1:])

        response = response.replace('.', '\n')
        for response_line in response.split('\n')[:5]:
            if response_line.strip() == "": continue
            response_replaced = response_line.lower().replace('jane street', 'optiver')
            await update.message.reply_text(response_replaced)
        if code is not None:
            await update.message.reply_text(code)

sampleData = None#sample encodings
def init():
    global sampleData
    if os.path.exists('presaved.dat'):
        file=open('presaved.dat','rb')
        sampleData = pickle.load(file)
        file.close()
        return None

    dir='sample_pics'
    img_files = [f'{dir}/{file}' for file in os.listdir(dir) if file!='.DS_Store']
    sampleData = []
    xx=[]
    yy=[]

    #process images one by one to reduce RAM consumed
    for filename in img_files:
        image = fr.load_image_file(filename)
        encoding = fr.face_encodings(image)
        for enc in encoding:sampleData.append(enc)
        # if len(encoding)!=1:print(filename, len(encoding))

    file=open('presaved.dat','wb')
    pickle.dump(sampleData,file)
    file.close()


def main() -> None:
    init()
    """Start the bot."""
    # Create the Updater and pass it your bot's token
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    assert(TELEGRAM_BOT_TOKEN is not None)
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(MessageHandler(None, reply))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
