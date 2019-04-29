# Reddit-Related-Articles
Reddit bot used to pull article titles and provide wikipedia descriptions of keywords.
Requires following dependencies: Flask, Reddit praw, wikipedia, textblob, and textblob.download_corpora (all available through pip)
The reddit bot configuration is blank as you must create your own bot to 
register it with reddit and the flask app through the config file.

In Future iterations of this project, the reddit bot and wikipedia python api will be replaced by json requests. But due to reddit's limitations on API usage and the need for OAUTH I used a bot instead for personal use and to be compliant with request maxes
