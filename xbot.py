import tweepy
import asyncio
from openai import OpenAI
from quart import Quart
import os
import logging
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        messages=[{"role": "user", "content": prompt}],
        model="gpt-3.5-turbo"
    )
    return chat_completion.choices[0].message.content  

async def tweet():
    while True:
        generated_message = generate_tweet(PROMPT)
        try:
            api.create_tweet(text=generated_message)
            logger.info("Tweeted: %s", generated_message)
        except tweepy.TweepyException as e:
            logger.error("Error: %s", e.reason)

        logger.info("Time until next tweet: 40min")
        await asyncio.sleep(2400)    

# Quart app
app = Quart(__name__)

# Route for handling HTTP requests
@app.route('/')
async def home():
    return 'Twitter bot is running!'

@app.before_serving
async def before_serving():
    # Start tweeting loop as a background task
    await asyncio.create_task(tweet())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
