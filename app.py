import os

from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'media/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    images = ['one', 'two', 'three']
    return render_template('index.html', images=images)


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files or 'title' not in request.form:
        app.logger.warning('Upload failed. No file or title was provided.')
        return redirect('/', code=302)

    title = request.form['title']
    file = request.files['file']

    if title == '':
        app.logger.warning('No title was provided.')
        return redirect('/', code=302)

    if file.filename == '':
        app.logger.warning('No file was provided.')
        return redirect('/', code=302)

    if not allowed_file(file.filename):
        app.logger.warning('Invalid file format. Allowed formats: ' + ', '.join(ALLOWED_EXTENSIONS) + '.')
        return redirect('/', code=302)

    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    app.logger.info(f'File has been successfully uploaded: {filename}.')
    return redirect('/', code=302)


if __name__ == '__main__':
    app.run()
