import tweepy
import json
import re
from dotenv import dotenv_values
config = dotenv_values(".env")

with open("data/dutch_names.json", 'r') as file:
    NAMES = json.load(file)

def has_numbers(twitter_handle):
    return any(char.isdigit() for char in twitter_handle)

def has_letters(twitter_handle):
    return any(char.isalpha() for char in twitter_handle)

def nameCheck(twitter_handle, amount_of_numbers):  # returns bool 
    if has_numbers(twitter_handle) == True:
        if has_letters(twitter_handle) == True:
            temp = re.compile("([a-zA-Z]+)([0-9]+)")    # Using re.compile() + re.match() + re.groups()
            res = temp.match(twitter_handle).groups()         # Splitting text and number in string
            numbercheck = res[1]
            numbercheck = len(numbercheck)
            if numbercheck >= amount_of_numbers:
                bunch_of_numbers = True
            else: 
                bunch_of_numbers = False
                return False
            if bunch_of_numbers == True:
                first_name = res[0]
                for name in NAMES:
                    if first_name == name["name"]:
                        return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else: 
        return False 

auth = tweepy.OAuthHandler(config["CONSUMER_KEY"], config["CONSUMER_KEY_SECRET"])
auth.set_access_token(config["ACCESS_TOKEN"], config["ACCESS_TOKEN_SECRET"])

api = tweepy.API(auth)
query = "Mijn 1ste vliegen zwammen, oh zo blij mee "

data = []

names = []

for tweets in tweepy.Cursor(api.search_tweets, q=query, count=30, lang="nl", result_type="latest").pages(1):
    for tweet in tweets:
        tweet = tweet._json
        twitter_handle = tweet["user"]["screen_name"]
        name_check = nameCheck(twitter_handle, 2)
        if name_check == True:
            print("We caught one!")
            data.append(tweet)
        else: 
            print("No Firstnames Bunchofnumbers found.")

filename = 'data/tweets_hash.json'
with open (filename, 'w') as outfile:
    json.dump(data, outfile)