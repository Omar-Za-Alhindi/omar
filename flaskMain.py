import concurrent.futures
import os

import flask
import werkzeug

import main

UPLOAD_FOLDER = '.'

app = flask.Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

result = ''

@app.route('/', methods=['GET', 'POST'])
def handle_request():
    imagefile = flask.request.files['image']
    filename = werkzeug.utils.secure_filename(imagefile.filename)
    print("\nReceived image File name : " + imagefile.filename)
    # imagefile.save(filename)

    imagefile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    global result

    with concurrent.futures.ThreadPoolExecutor() as executer:
        f1 = executer.submit(main.main, filename)
        result, headers = f1.result()

    print (main.resultString(result, headers))
    return main.resultString(result, headers)


@app.route('/result/', methods=['GET', 'POST'])
def result_request():
    req = flask.request.get_json()
    print('req')
    if main.returnResult() != '':
        return main.returnResult()
    return 'processing'


app.run(host="0.0.0.0", port=5000, debug=True)
