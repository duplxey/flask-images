import os
import sqlite3
from flask import Flask, send_from_directory
from flask import redirect
from flask import render_template
from flask import request
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'x&7znvo5yo!)04p62qiicm2o_dt560wdt+$q_7t+(94w$c*zhg'
app.config['UPLOAD_FOLDER'] = 'media/'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/media/<path:path>')
def media(path):
    return send_from_directory(app.config['UPLOAD_FOLDER'], path)


@app.route('/')
def index():
    conn = get_db_connection()
    images = conn.execute('SELECT * FROM images ORDER BY uploaded_at DESC').fetchall()
    conn.close()
    return render_template('index.html', images=images)


@app.route('/upload', methods=['POST'])
def upload():
    title = request.form['title']
    file = request.files['file']

    if not title or not file or title == '' or file.filename == '':
        app.logger.warning('No title or file were provided.')
        return redirect('/', code=302)

    if not allowed_file(file.filename):
        app.logger.warning('Invalid file format. Allowed formats: ' + ', '.join(ALLOWED_EXTENSIONS) + '.')
        return redirect('/', code=302)

    # save the file to the UPLOAD_FOLDER
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # add an entry to the database
    conn = get_db_connection()
    conn.execute('INSERT INTO images(title, file) VALUES (?, ?)', (title, filename))
    conn.commit()
    conn.close()

    app.logger.info(f'File {filename} has been successfully uploaded.')
    return redirect('/', code=302)


if __name__ == '__main__':
    app.run()
