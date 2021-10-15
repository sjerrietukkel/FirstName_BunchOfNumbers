import tweepy
import json
import re
from dotenv import dotenv_values
config = dotenv_values(".env")

with open("data/dutch_names.json", 'r') as file:
    names = json.load(file)

# initializing string 
test_str = "Bert9498"

def has_numbers(twitter_handle):
    return any(char.isdigit() for char in twitter_handle)

def nameCheck(twitter_handle):  
    if has_numbers(twitter_handle) == True:
        temp = re.compile("([a-zA-Z]+)([0-9]+)")    # Using re.compile() + re.match() + re.groups()
        res = temp.match(twitter_handle).groups()         # Splitting text and number in string
        numbercheck = res[1]
        numbercheck = len(numbercheck)
        if numbercheck > 3:
            bunch_of_numbers = True
        else: 
            bunch_of_numbers = False
        for name in names:
            name = name["name"]
            first_name = False
            if res[0] == name:
                first_name = True
            if first_name == True and bunch_of_numbers == True:
                return True
            elif first_name == False or bunch_of_numbers == False:
                return False
    else: 
        return False 

# nameCheck(test_str)
print(nameCheck(test_str))

auth = tweepy.OAuthHandler(config["CONSUMER_KEY"], config["CONSUMER_KEY_SECRET"])
auth.set_access_token(config["ACCESS_TOKEN"], config["ACCESS_TOKEN_SECRET"])

api = tweepy.API(auth)
# screen_name = "nos"
query = "#me2"

data = []

names = []

# for tweets in tweepy.Cursor(api.search_tweets, q=query, count=30, lang="nl", result_type="recent").pages(1):
#     for tweet in tweets:
#         tweet = tweet._json
#         if tweet["user"]["name"] == "WappieNL":
#             data.append(tweet)

# filename = 'data/tweets_hash.json'
# with open (filename, 'w') as outfile:
#     json.dump(data, outfile)