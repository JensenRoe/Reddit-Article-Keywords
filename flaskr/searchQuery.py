import functools
from . import reddit_data
from flask import (
    Blueprint, flash, current_app, redirect, render_template, request, url_for, Flask
)

bp = Blueprint('searchQuery', __name__)

DEFAULT_SEARCH_LIMIT = 5

@bp.route('/search_query', methods=('GET', 'POST'), )
def searchQuery():
    if request.method == 'POST':
        search_query = request.form['subreddit']
        search_query_limit = request.form['search_query_limit']
        search_query_limit = int(search_query_limit)
        reddit = reddit_data.bot_login()
        error = None

        if (not search_query_limit):
            search_query_limit = DEFAULT_SEARCH_LIMIT
        elif(search_query_limit > 20):
            search_query_limit = 20
            
        if (not searchQuery):
            error = 'subreddit name is required'
            
        related_articles_arrays = reddit_data.run_bot(reddit , search_query , search_query_limit)
        related_articles = related_articles_arrays[0]
        title_array = related_articles_arrays[1]
        permalinks_array = related_articles_arrays[2]
        if (related_articles_arrays is None):
            error = 'subreddit does not exist or is mispelled, make sure not to add /r/ and that it is just the name of the subreddit'
        if (error is None):

            return render_template('results.html', related_articles=related_articles ,
                            title_array=title_array , permalinks_array=permalinks_array)

        flash(error)
    #needs to be changed
    return render_template('search_query.html')
