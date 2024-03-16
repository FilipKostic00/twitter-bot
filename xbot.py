import tweepy
import time
from openai import OpenAI
from quart import Quart

import os
from dotenv import load_dotenv

load_dotenv()

# Twitter API credentials
ACCESS_KEY = os.getenv('ACCESS_KEY')
ACCESS_SECRET = os.getenv('ACCESS_SECRET')
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
BEARER_TOKEN = os.getenv('BEARER_TOKEN')

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

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
    api_key=OPENAI_API_KEY
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

# Quart app
app = Quart(__name__)

# Route for handling HTTP requests
@app.route('/')
async def home():
    return 'Twitter bot is running!'

if __name__ == '__main__':
    # Start tweeting
    tweet()
    # Start the Quart app on the specified port
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
