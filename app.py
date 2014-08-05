#pip includes
from flask import Flask, session, redirect, url_for, escape, request, render_template
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

from werkzeug.utils import secure_filename

#main python includes
import datetime, uuid, os, ConfigParser

#local python includes
import parser

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

Base = declarative_base()
UPLOAD_PATH = '/home/brianherman/kml/static/' 
engine = create_engine('sqlite:///tokens.db')
class Token(Base):
    __tablename__ = 'token'
    uuid = Column(String, primary_key=True)
    expire = Column(DateTime, default=datetime.datetime.utcnow)


app = Flask(__name__)
@app.route('/static/<path:filename>')
def send_foo(filename):
    return send_from_directory('static', filename)
@app.route("/")
def index():
    session['token'] = uuid.uuid4()
    the_token = Token(uuid = session['token'],expire=datetime.datetime.utcnow) 
    return render_template('index.html', token=session['token'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            os.mkdir(os.path.join(UPLOAD_PATH,str(session['token'])),777)
            file.save(os.path.join(UPLOAD_PATH,str(session['token']),'upload.json'))
#            parser.load(os.path.join(UPLOAD_PATH,str(session['token']),'upload.json'),\
#                        os.path.join(UPLOAD_PATH,str(session['token']),'upload.kml'))
#            splitter.load(os.path.join(UPLOAD_PATH,str(session['token'])+'upload.kml'),\
#                          os.path.join(str(session['token'])))
    return render_template("view.html")

@app.route('/viewme/<number>')
def viewme(number=None):
    return render_template('view.html', number=number)
@app.route('/view')
def view():
    username = request.cookies.get('token')
    big_file = '/home/brianherman/static/'+session['token']+'/upload.json'
    
@app.route('/quit')
def quit():
    # remove the username from the session if it's there
    session.pop('token', None)
    return redirect(url_for('index'))

# get the secret key from configuration.  keep this really secret:

with open('secret_key.txt', 'r') as key_file:
    secret_key = key_file.read()
    app.secret_key = secret_key 

if __name__ == "__main__":
#    app.run(host='0.0.0.0', debug=True, port=5000)
#    app.run(host='0.0.0.0', debug=True, port=80)
