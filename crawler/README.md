Mastodon Crawler README
Description
This script is a Mastodon crawler that collects statuses from the public timeline, processes the statuses for Natural Language Processing (NLP), and saves them into a CouchDB database. The script uses several pre-trained models from the transformers library to analyze the sentiment and toxicity of the statuses. It also makes use of the HuggingFace API for sentiment classification. The script is designed to be robust and tries to handle all kinds of unexpected errors gracefully.

Setup and Installation
Before running this script, make sure you have the required dependencies installed. You can install the necessary packages using pip:

bash
Copy code
pip install mastodon.py couchdb python-dotenv transformers torch nltk bs4 langdetect emoji requests
Make sure you have CouchDB installed and running, and you have your admin credentials.

Usage
Before running the script, make sure to modify these variables according to your needs:

admin: The username for your CouchDB admin.
password: The password for your CouchDB admin.
url: The URL of your CouchDB instance.
db_name: The name of the CouchDB database where the statuses will be stored.
token: The token for your Mastodon account (you may want to use an environment variable to store this).
api_base_url: The base URL for your Mastodon instance.
Next, simply run the script:

bash
Copy code
python crawler.py
How It Works
The script logs into your Mastodon account and listens for new statuses on the public timeline. When it receives a status, it adds it to a buffer. When the buffer size reaches 50, the script processes the statuses in the buffer as follows:

It removes HTML tags, URLs, emojis, and non-alphanumeric characters.
It tokenizes the text and removes English stop words, punctuation, and applies lemmatization.
It calculates the toxicity of the text using a pre-trained model.
It calculates the sentiment of the text using a pre-trained model from HuggingFace API.
After processing, the script checks if the status is in English and if so, it saves the processed status to the CouchDB database along with followers and following count of the user who posted it.

Caution
This script contains sensitive information such as CouchDB and Mastodon credentials. Be sure to keep this information secure, and do not share this script publicly without removing this information.

Remember to respect the privacy and terms of service of the Mastodon instance you are crawling. Always get proper permissions before crawling or storing data.

Contributors
This script was created as a part of an open-source project. We appreciate contributions. If you found a bug or want to propose a feature, feel free to do so.
