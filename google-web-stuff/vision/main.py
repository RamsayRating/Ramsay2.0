import base64
import os

from flask import Flask, redirect, render_template, request
from Ramsay2.food_recognition import what_object
from .gordon_twitter import retrieve_tweet_database, connect_to_database
from werkzeug.utils import secure_filename

#CHANGE THIS TO YOUR OWN PATH
UPLOAD_FOLDER = '/Users/emilylepert/Documents/Olin_2/HackHarvard/Ramsay2.0/resources'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def homepage():
    # Return a Jinja2 HTML template.
    return render_template('homepage.html', image_entities=image_entities)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_photo', methods=['GET','POST'])
def upload_photo():
    # Create a Cloud Storage client.
    
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        score = what_object(name_file)
        conn = connect_to_database()
        tweet = ''
        if score > 0.75:
            tweet = retrieve_tweet_database(conn,1.0)
        else:
            tweet = retrieve_tweet_database(conn,2.0)

    return render_template('secondpage.html', tweet=tweet)


@app.errorhandler(500)
def server_error(e):
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)