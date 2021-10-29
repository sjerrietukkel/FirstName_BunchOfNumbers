import string, tweepy, json, re
from dotenv import dotenv_values
from sentiment import analyze_sentiment, translate_text
from nltk.tokenize import WordPunctTokenizer

config = dotenv_values(".env")
auth = tweepy.OAuthHandler(config["CONSUMER_KEY"], config["CONSUMER_KEY_SECRET"])
auth.set_access_token(config["ACCESS_TOKEN"], config["ACCESS_TOKEN_SECRET"])
api = tweepy.API(auth)

query = "nieuwsuur"
data = []

with open("names/dutch_names.json", 'r') as file:
    NAMES = json.load(file)

def has_numbers(twitter_handle):
    return any(char.isdigit() for char in twitter_handle)

def has_letters(twitter_handle):
    return any(char.isalpha() for char in twitter_handle)

def starts_with_numb(twitter_handle): #Had a bug where strings that started with an int broke the query
    return twitter_handle[0].isdigit() 

def clean_tweets(tweet):
    user_removed = re.sub(r'@[A-Za-z0-9]+','',tweet)
    link_removed = re.sub('https?://[A-Za-z0-9./]+','',user_removed)
    number_removed = re.sub('[^a-zA-Z]', ' ', link_removed)
    lower_case_tweet= number_removed.lower()
    tok = WordPunctTokenizer()
    words = tok.tokenize(lower_case_tweet)
    clean_tweet = (' '.join(words)).strip()
    return clean_tweet

def nameCheck(twitter_handle, amount_of_numbers):  # returns bool 
    if starts_with_numb(twitter_handle) == False:
        if has_numbers(twitter_handle) == True:
            if has_letters(twitter_handle) == True:
                temp = re.compile("([a-zA-Z]+)([0-9]+)")    # Using re.compile() + re.match() + re.groups()
                res = temp.match(twitter_handle).groups()         # Splitting text and number in string
                print(res)
                numbercheck = res[1]
                numbercheck = len(numbercheck)
                if numbercheck >= amount_of_numbers:
                    bunch_of_numbers = True
                else: 
                    bunch_of_numbers = False
                    return False, 0
                if bunch_of_numbers == True:
                    first_name = res[0]
                    for name in NAMES:
                        if first_name == name["name"]:
                            gender = name["gender"]
                            return True, gender
                    else:
                        return False, 0
                else:
                    return False, 0
            else:
                return False, 0
        else: 
            return False, 0
    else: 
        return False, 0

for tweets in tweepy.Cursor(api.search_tweets, q=query, count=100, lang="nl", tweet_mode='extended', result_type="latest").pages(5):
    total = 0
    total_found = 0
    for tweet in tweets:
        tweet = tweet._json
        twitter_handle = tweet["user"]["screen_name"]
        twitter_handle = ''.join(filter(str.isalnum, twitter_handle))
        print(twitter_handle)
        name_check_pass, gender = nameCheck(twitter_handle, 2)
        total = total + 1
        if name_check_pass == True:
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
                    'gender' : gender,
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
                    'gender' : gender,
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
filename = 'data/tweets_' + query +'.json'
with open (filename, 'w', encoding='utf8') as outfile:
    json.dump(data, outfile)
