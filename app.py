import requests
from flask import Flask, request, render_template, flash, redirect, send_from_directory, abort

from iiif_utils import *

app = Flask(__name__)


@app.route('/uv/<path:path>')
def send_js(path):
    return send_from_directory("uv", path)


def display_iiif(manifest_filename):  # todo 6/16/21 kelleylynch support a list of filenames
    manifest_filename = os.path.basename(manifest_filename)
    return render_template('player_page.html', manifest=manifest_filename)


@app.route('/display')
def display_file():
    try:
        mmif_str = requests.get(request.args["file"]).text
        manifest_filename = generate_iiif_manifest(mmif_str)
    except:
        return abort(404)
    return display_iiif(manifest_filename)


def upload_display(mmif: Mmif):
    '''
    :param mmif:
    :return:
    '''
    manifest_filename = generate_iiif_manifest(mmif)
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
            # filename = secure_filename(file.filename)
            # file.save(os.path.join('temp', filename))
            mmif = Mmif(file.read())
            return upload_display(mmif)
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
    app.run(host="0.0.0.0")
