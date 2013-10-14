from datetime import datetime
from flask import Flask, render_template, request
from flask.ext.pymongo import PyMongo
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import TextField, SubmitField
from bson.objectid import ObjectId

app = Flask(__name__)
app.config.from_object('config')
mongo = PyMongo(app)
bootstrap = Bootstrap(app)

MONGO_DBNAME = 'qdb'

@app.route('/qdb/')
@app.route('/qdb/<qid>/')
def display(qid=None):
    if qid:
        quote = mongo.db.quotes.find_one(ObjectId(qid))
    else:
        quote = mongo.db.quotes.find_one()
    return render_template('display.html', quote=quote)

@app.route('/qdb/submit/')
def submit():
    form = SubmissionForm()
    return render_template('submit.html', form=form)

@app.route('/qdb/submitted/', methods = ['GET', 'POST'])
def submitted():
    if request.method == 'POST':
        data = {'text': request.form['text'], 'author': request.form['author'],
                'tags': request.form['tags'].split(','), 'time':
                str(datetime.now()), 'upvotes': 0, 'downvotes': 0, 'score': 0}
        qid = mongo.db.quotes.insert(data)
        link = '/qdb/%s/' % str(qid)
        return render_template('submitted.html', link=link)
    # TODO - why doesn't this redirect to oops.html?
    return render_template('oops.html')


class SubmissionForm(Form):
    text = TextField('Quote')
    author = TextField('Submitted by')
    tags = TextField('Tags (separate with commas)')
    submit_button = SubmitField('Submit Form')

if __name__ == '__main__':
    app.debug = True
    app.run()
