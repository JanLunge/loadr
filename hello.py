from flask import Flask
import sys, os
from flask import request
from flask import render_template

app = Flask(__name__)
downloads = 0
@app.route("/")
def addToQueue():
    return render_template('add-to-queue.html')

@app.route("/load")
def load():
    os.system("sh load.sh video")
    downloads = downloads + 1
    return render_template('status.html')

@app.route('/log', methods=['POST', 'GET'])
def status():
    os.system("echo " + request.form['url'] + " >> batches/" + request.form['type'] + ".txt")
    batch=os.popen("cat batch.txt").read()
    return render_template('stats.html', batch=batch)
    return "<a href='/'>more</a> -- <a href='/load'>load</a><br>" + os.popen("cat batch.txt").read()

@app.route('/api/status')
def apiStatus():
    batches=os.popen("ls batches").read()
    return "<a href='/'>more</a> -- <a href='/load'>load</a><hr>" + batches + "<hr>" + str(downloads)
    return render_template('stats.html', batch=batches)
