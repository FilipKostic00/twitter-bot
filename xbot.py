import tweepy
import time
from openai import OpenAI

#Client ID = "ajltbEtaNG9GMmRhQ1dpQzFqSVk6MTpjaQ"
#Client Secret = "005fce_KE3CFIfXlLkuG7cXqDPhJnDimOcW51UVBjLD66XpoiC"

# Twitter API credentials
ACCESS_KEY = '1749892773195522048-pL4Kz3t4faF8Lz0cgManudVpaq8mEH'
ACCESS_SECRET = '8mSeBSQI5S7nLyeVeZXaIXjizzgw60Zh2MZI5CHcx1dZg'
CONSUMER_KEY='AQsD4HAiVaBzANK8ixTysD5nm'
CONSUMER_SECRET='mxkps0IontaFDSEO391f8RgTUTyxnbCzL7z4CjyOgt5DF02ORG'
BEARER_TOKEN ='AAAAAAAAAAAAAAAAAAAAAHYRswEAAAAAjdtMR2l%2FthncqWuSTCRlGmsI6jU%3DCj2t5oa0F22dPYixE49OzcEDzr4KWAFl4KKA7xBNDvzngELlZq'

#PROMPT
PROMPT = 'Write me a tweet about farming crypto coin $BLOCK.Needs to sound passionate about new coin. Maybe show some excitement .Needs to be short, max 30 words. Use emojis.Try to use $BLOCK in a sentence .It also needs to include @GetBlockGames at the end. '

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


while True:
    print("Do you want to start twitter bot [Y/N]")
    response = input()

    if (response.upper() == "Y"):
        print("Twitter bot is starting...")
        print("Tweets should start appearing soon")
        tweet()
    elif (response.upper() == "N"):
        print("Goodbye!")
        break
    else :
        print("Type 'Y' for Yes and 'N' for No")
    