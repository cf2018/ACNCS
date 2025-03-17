from flask import render_template, request, redirect, url_for
from app import app
from app.utils import allowed_file, process_image
import os

UPLOAD_FOLDER = 'app/static/uploads'
PROCESSED_FOLDER = 'app/static/uploads/processed'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/ping', methods=['GET'])
def ping():
    return 'pong'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            processed_image_path, calculation = process_image(file_path)
            return render_template('result.html', original_image=file_path, processed_image=processed_image_path, calculation=calculation)
    images = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', images=images)

@app.route('/analyze/<filename>')
def analyze(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    processed_image_path, calculation = process_image(file_path) , 'Calculated value'
    return render_template('result.html', original_image=file_path, processed_image=processed_image_path, calculation=calculation)