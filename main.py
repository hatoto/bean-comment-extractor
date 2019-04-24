from flask import Flask, render_template, request, redirect, url_for
import os
from beanParser import parseBeanField
import logging


ALLOWED_EXTENSIONS = set(['txt', 'java'])

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uploadajax', methods=['GET', 'POST'])
def upload_file():
    fileContent = ''
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            
            filename = file.filename
            fileStr = file.read().decode("utf-8")            
            fileContent = fileStr.splitlines()            
            app.logger.info('%s uploaded file: %s', request.remote_addr, filename)         

            return parseBeanField(fileContent)
            
    return ''


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(threaded=True)


if __name__ != '__main__':
    gunicorn_logger=logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)