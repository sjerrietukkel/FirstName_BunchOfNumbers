import string, tweepy, json, re
from dotenv import dotenv_values
from sentiment import analyze_sentiment, translate_text
from nltk.tokenize import WordPunctTokenizer

config = dotenv_values(".env")
auth = tweepy.OAuthHandler(config["CONSUMER_KEY"], config["CONSUMER_KEY_SECRET"])
auth.set_access_token(config["ACCESS_TOKEN"], config["ACCESS_TOKEN_SECRET"])
api = tweepy.API(auth)

query = "klimaat" 
data = []

with open("names/dutch_names.json", 'r') as file:
    NAMES = json.load(file)

def clean_tweets(tweet):
    user_removed = re.sub(r'@[A-Za-z0-9]+','',tweet)
    link_removed = re.sub('https?://[A-Za-z0-9./]+','',user_removed)
    number_removed = re.sub('[^a-zA-Z]', ' ', link_removed)
    lower_case_tweet= number_removed.lower()
    tok = WordPunctTokenizer()
    words = tok.tokenize(lower_case_tweet)
    clean_tweet = (' '.join(words)).strip()
    return clean_tweet

for tweets in tweepy.Cursor(api.search_tweets, q=query, count=100, lang="nl", tweet_mode='extended', result_type="latest").pages(5):
    total = 0
    total_found = 0
    for tweet in tweets:
        tweet = tweet._json
        twitter_handle = tweet["user"]["screen_name"]
        twitter_handle = ''.join(filter(str.isalnum, twitter_handle))
        print(twitter_handle)
        total = total + 1
        print("We caught one!")
        text = tweet["full_text"]
        rt = text.startswith('RT')
        print("")
        if rt == True:
            text = tweet["retweeted_status"]["full_text"]
            translation = translate_text('en', text)
            clean_tweet = clean_tweets(translation)
            sentiment = analyze_sentiment(clean_tweet)
            print(sentiment)
            total_found = total_found + 1
            data.append({   
                'query': query,
                'date' : tweet["created_at"],
                'screen_name' : tweet["user"]["screen_name"],
                'gender' : "unknown",
                'text' : tweet["retweeted_status"]["full_text"],
                "followers" : tweet["user"]["followers_count"],
                "retweet" : True,
                "original_author" : tweet["retweeted_status"]["user"]["screen_name"],
                "sentiment" : sentiment[0],
                "magnitude" : sentiment[1]
            })
            print("Retweet is trueee") 
        else:
            text = tweet["full_text"]
            translation = translate_text('en', text)
            clean_tweet = clean_tweets(translation)
            sentiment = analyze_sentiment(clean_tweet)
            total_found = total_found + 1
            data.append({
                'query': query,
                'date' : tweet["created_at"],
                'screen_name' : tweet["user"]["screen_name"],
                'gender' : "unknown",
                'text' : tweet["full_text"],
                "followers" : tweet["user"]["followers_count"],
                "retweet" : False,
                "original_author" : tweet["user"]["screen_name"],
                "sentiment" : sentiment[0],
                "magnitude" : sentiment[1]
            })
    else: 
        print("No Firstnames Bunchofnumbers found.")
        

print(total)
filename = 'data/tweets_all_' + query +'.json'
with open (filename, 'w', encoding='utf8') as outfile:
    json.dump(data, outfile)
