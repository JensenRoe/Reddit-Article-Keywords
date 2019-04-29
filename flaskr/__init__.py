from flask import (Flask, render_template, redirect, url_for)

app = Flask(__name__)

from . import searchQuery
app.register_blueprint(searchQuery.bp)

@app.route('/' , methods=['GET', 'POST'])
def index():
    return redirect(url_for('searchQuery'))

@app.route('/search_query', methods=['GET', 'POST'])
def searchQuery():
    return render_template('search_query.html')

if (__name__ == "__main__"):
    app.run()
