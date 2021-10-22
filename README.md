# FirstName BunchOfNumbers Detector

### Installation

```bash
git clone
pip install tweepy
pip install dotenv
pip install google-cloud
```

Request api keys: https://developer.twitter.com/ \
Store keys in `.env`.

```env
CONSUMER_KEY = 'YOUR_KEY'
CONSUMER_KEY_SECRET = 'YOUR_KEY'
ACCESS_TOKEN = 'YOUR_KEY'
ACCESS_TOKEN_SECRET = 'YOUR_KEY'
```

Request cloud console key key: https://cloud.google.com/storage/docs/reference/libraries \
Store json as `creds.json` in root. \
Navigate to folder and run (bash)

```bash
export GOOGLE_APPLICATION_CREDENTIALS='creds.json'
python final.py
```
