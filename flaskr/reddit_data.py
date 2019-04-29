from . import reddit_config
import praw
from praw.models import Submission
from textblob import TextBlob
import wikipedia

def bot_login():
    #initializes an empty array to store 
    title_arr = []

    #Logs into reddit through our scraping account
    reddit = praw.Reddit(username = reddit_config.username,
                         password = reddit_config.password,
                         client_id = reddit_config.client_id,
                         client_secret = reddit_config.client_secret,
                         user_agent = "CoolGuyMoz article finder v0.1")
    return reddit



def run_bot(reddit , subreddit_name , post_limit):
    title_arr = []
    textblob_title_arr = []
    permalink_arr = []
    if(subreddit_exists(subreddit_name)):
        subreddit = reddit.subreddit(subreddit_name)
    else:
        return none
    
    for post in subreddit.hot(limit = post_limit):      #grabs first 10 posts from "hot" tab            
        title_arr.append(post.title)
        textblob = TextBlob(post.title)            #turns raw str into textblob obj
        permalink = "https://www.reddit.com"
        permalink += post.permalink
        permalink_arr.append(permalink)
        textblob_title_arr.append(textblob.tags)
    pnoun_extract_arr = extract_proper_nouns(textblob_title_arr)
    wiki_summaries = get_wiki_summaries(pnoun_extract_arr)
    return (wiki_summaries , title_arr , permalink_arr)
    
reddit = bot_login()

def is_proper_noun(word):
    return word[1] == "NNP" or word[1] == "NNPS"

def subreddit_exists(subreddit_name):
    valid_subreddit = True
    try:
        subreddit = reddit.subreddit(subreddit_name)
    except:
        valid_subreddit = False
    return valid_subreddit

def extract_proper_nouns(title_arr):
    #Initializes empty list to contain only proper noun words from each title
    pnoun_title_arr = []
    
    for title in title_arr:
        raw_tuple_index = 0 #word in title
        pnoun_title_words = [] #proper nouns in title
        pnoun_title_words_size = 0 #size of array
        for raw_tuple_index in range(len(title)):
            proper_noun = title[raw_tuple_index][0]
            #if previous word is also proper noun, assume continuous proper noun e.g: Mexico City
            if( raw_tuple_index > 0 and is_proper_noun(title[raw_tuple_index - 1]) and
                is_proper_noun(title[raw_tuple_index]) ):
                pnoun_title_words[pnoun_title_words_size - 1] += ' ' + title[raw_tuple_index][0]
            
            #if word is a proper noun, append
            elif( is_proper_noun(title[raw_tuple_index]) ):
                pnoun_title_words.append(proper_noun)
                pnoun_title_words_size += 1
                
            
        pnoun_title_arr.append(pnoun_title_words)


    return pnoun_title_arr


def get_wiki_summaries( pnoun_keywords_array ):
    wiki_summaries = []
    for title in pnoun_keywords_array:
        current_wiki_summaries = []
        for word in title:
            try:
                search_results = wikipedia.search(word)
                summary = wikipedia.summary( search_results[0] , sentences=2)
            except:
                summary = ''
            current_wiki_summaries.append(summary)
        wiki_summaries.append(current_wiki_summaries)
    return wiki_summaries
