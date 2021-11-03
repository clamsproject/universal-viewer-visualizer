import requests

from flask import Flask, request, render_template, flash, redirect, send_from_directory
from werkzeug.utils import secure_filename

from iiif_utils import *

app = Flask(__name__)


@app.route('/uv/<path:path>')
def send_js(path):
    return send_from_directory("uv", path)


@app.route('/temp/<path:path>')
def send_temp(path):
    return send_from_directory("temp", path)


@app.route('/alto/<path:path>')
def send_alto(path):
    return send_from_directory("../data/alto", path)


@app.route('/mmif/<path:path>')
def send_mmif(path):
    return send_from_directory("../data/mmif", path)


def display_iiif(manifest_filename):  # todo 6/16/21 kelleylynch support a list of filenames
    manifest_filename = os.path.basename(manifest_filename)
    return render_template('player_page.html', manifest=manifest_filename)


@app.route('/display')
def display_file():
    try:
        mmif_str = requests.get(request.args["file"]).text
        manifest_filename = generate_iiif_manifest(mmif_str)
    except:
        manifest_filename = "static/old_manifest.json"
    return display_iiif(manifest_filename)


def upload_display(filename: str):
    '''
    :param filename:
    :return:
    '''
    manifest_filename = generate_iiif_manifest(open(os.path.join("temp", filename)).read())
    return display_iiif(manifest_filename)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join('temp', filename))
            return upload_display(filename)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form> 
    '''


if __name__ == '__main__':
    app.run()
