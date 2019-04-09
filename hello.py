from flask import Flask
import sys, os
from flask import request
from flask import render_template
from flask import json
app = Flask(__name__)
downloads = 0
types= [
    {"label": "Video", "value": "video"},
    {"label": "Music", "value": "music"},
    {"label": "Other", "value": "hidden"},
]
@app.route("/")
def addToQueue():
    return render_template('add-to-queue.html', types=types)

@app.route("/load/<type>")
def load(type):
    os.system("sh load.sh " + type)
    return render_template('status.html')

@app.route('/log', methods=['POST', 'GET'])
def status():
    os.system("echo " + request.form['url'] + " >> batches/" + request.form['type'] + ".txt")
    batch=os.popen("cat batch.txt").read()
    return render_template('stats.html', batch=batch)
    return "<a href='/'>more</a> -- <a href='/load'>load</a><br>" + os.popen("cat batch.txt").read()

# available batches
@app.route('/api/batches')
def apiStatusBatches():
    batchesCli=os.popen("ls batches | sed -e 's/\.txt$//;s/$/\",/;s/^/\"/;$ s/.\{1\}$//'").read()
    batches = '{ "batches": [' + batchesCli + "]}"
    response = app.response_class(
        response=batches,
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/api/batch/<name>')
def apiStatusBatch(name):
    batches=os.popen("cat batches/"+name+".txt | wc -l").read()
    batches = '{ "lineCount": ' + batches + "}"
    response = app.response_class(
        response=batches,
        status=200,
        mimetype='application/json'
    )
    return response
