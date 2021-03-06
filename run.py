from herokuflask import app
app.debug = os.getenv('FLASK_DEBUG') != 'False'  # updates the page as the code is saved
HOST = '0.0.0.0' if 'PORT' in os.environ else '127.0.0.1'
PORT = int(os.environ.get('PORT', 3000))
app.run(host='0.0.0.0', port=PORT)
