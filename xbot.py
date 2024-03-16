import tweepy
import time
from openai import OpenAI

import os
from dotenv import load_dotenv

load_dotenv()

# Twitter API credentials
ACCESS_KEY = os.getenv('ACCESS_KEY')
ACCESS_SECRET = os.getenv('ACCESS_SECRET')
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
BEARER_TOKEN = os.getenv('BEARER_TOKEN')

#PROMPT
PROMPT = os.getenv('PROMPT')

# Authenticate to Twitter
auth = tweepy.OAuth1UserHandler(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)
oldapi = tweepy.API(auth)
api = tweepy.Client(bearer_token=BEARER_TOKEN,
                    consumer_key=CONSUMER_KEY, 
                    consumer_secret=CONSUMER_SECRET, 
                    access_token = ACCESS_KEY, 
                    access_token_secret= ACCESS_SECRET
                    )

client = OpenAI(
    api_key="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"
)

def generate_tweet(prompt):
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="gpt-3.5-turbo",
    )
    return chat_completion.choices[0].message.content  

def tweet():
    while True:
        generated_message = generate_tweet(PROMPT)
        try:
            api.create_tweet(text=generated_message)
            print("Tweeted:", generated_message)
        except tweepy.TweepyException as e:
            print("Error:", e.reason)

        #Print time left for next tweet    
        for i in range(3600,0,-1):
            time.sleep(1)
            print("Time until next tweet: " + f"{int(i/60)}" + "min", end="\r", flush=True)

#For Desktop use

# while True:
#     print("Do you want to start twitter bot [Y/N]")
#     response = input()

#     if (response.upper() == "Y"):
#         print("Twitter bot is starting...")
#         print("Tweets should start appearing soon")
#         tweet()
#     elif (response.upper() == "N"):
#         print("Goodbye!")
#         break
#     else :
#         print("Type 'Y' for Yes and 'N' for No")

#For web service use
tweet()    