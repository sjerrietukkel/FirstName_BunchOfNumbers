# FirstName BunchOfNumbers Detector

### Installation

```bash
git clone
pip install tweepy
pip install dotenv
pip install google-cloud google-cloud-translate==2.0.1
pip install dash dash-renderer dash_html_components dash_core_components
```

Request api keys: https://developer.twitter.com/ \
Store keys in `.env`.

```bash
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
