from flask import Flask, render_template
from flask.ext.pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
mongo = PyMongo(app)

MONGO_DBNAME = 'qdb'

@app.route('/qdb/')
@app.route('/qdb/<qid>/')
def qdb(qid=None):
    if qid:
        quote = mongo.db.quotes.find_one(ObjectId(qid))
    else:
        quote = mongo.db.quotes.find_one()
    return render_template('display.html', quote=quote)

if __name__ == '__main__':
    app.debug = True
    app.run()
