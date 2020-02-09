from app import app
from flask import render_template
import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, send_file
from werkzeug.utils import secure_filename
from .segmentation import Segmentator

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Эльдар Рязанов'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }, 
        {
            'author': {'username': 'Ипполит'},
            'body': 'Какая гадость эта ваша заливная рыба!!'
        }
    ]
    return render_template('index.html', user=user, posts=posts)


@app.route('/about')
def about():
    return 'aboutpage'


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
            file.save(os.path.join('static/uploads', filename))
            Segmentator(os.path.join('static/uploads', filename))
            return redirect('/images/' + filename)
    return render_template('upload.html')


@app.route('/images')
def list_images():
    files = os.listdir('static/uploads')
    return render_template('images.html', files=files)

@app.route('/images/<img_id>')
def show_image(img_id):
    img = '/uploads/' + img_id
    segments = '/segmented/' + img_id
    return render_template('image_compare.html', img=img, segments=segments)


@app.route('/uploads/<img_id>')
def static_from_root(img_id):
    print('Request for:', img_id)
    return send_file('../static/uploads/'+img_id)


@app.route('/segmented/<img_id>')
def segm_from_root(img_id):
    print('Request for:', img_id)
    return send_file('../static/segmented/'+img_id)
