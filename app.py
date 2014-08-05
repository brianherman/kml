#pip includes
from flask import Flask, session, redirect, url_for, escape, request, render_template
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

from werkzeug.utils import secure_filename

#main python includes
import datetime, uuid, os, ConfigParser

#local python includes
from parser import Parse 
from split import split 

ALLOWED_EXTENSIONS = set(['kml'])
UPLOAD_PATH='/home/brianherman/kml/static'
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
<<<<<<< HEAD
=======
    file = request.files['file']
>>>>>>> 44ab447a10c683fcea2d59a9bb60946080fbd3ca
    if request.method == 'POST':
        if file and allowed_file(file.filename):
<<<<<<< HEAD
            os.mkdir(os.path.join(UPLOAD_PATH,str(session['token'])),777)
            file.save(os.path.join(UPLOAD_PATH,str(session['token']),'upload.json'))
#            parser.load(os.path.join(UPLOAD_PATH,str(session['token']),'upload.json'),\
#                        os.path.join(UPLOAD_PATH,str(session['token']),'upload.kml'))
#            splitter.load(os.path.join(UPLOAD_PATH,str(session['token'])+'upload.kml'),\
#                          os.path.join(str(session['token'])))
    return render_template("view.html")
=======
          if not os.path.exists(os.path.join(UPLOAD_PATH,str(session['token']))):
              os.mkdir(os.path.join(UPLOAD_PATH,str(session['token'])))
              os.chmod(os.path.join(UPLOAD_PATH,str(session['token'])),0777)
          file.save(os.path.join(UPLOAD_PATH,str(session['token']),'upload.json'))
          the_parser = Parse()
          file_to_parse = os.path.join( UPLOAD_PATH,str(session['token']), 'upload.json' )
          result        = os.path.join(UPLOAD_PATH,str(session['token']),'upload.kml')
          user_dir   = os.path.join(UPLOAD_PATH,str(session['token']))
          print file_to_parse
          the_splitter = Splitter()
          the_parser.load(file_to_parse,result)
          splitter.load(result,user_dir)
#            os.mkdir('/home/brianherman/kml/static/'+str(session['token']),777)
#            file.save('/home/brianherman/kml/static/'+str(session['token'])+'/upload.json')
#            parser.load('/home/brianherman/kml/static/'+str(session['token'])+'upload.json',\
#                        '/home/brianherman/kml/static'/+str(session['token'])+'upload.kml')
#            splitter.load('/home/brianherman/kml/static/'+str(session['token'])+'upload.kml',\
#                          '/home/brianherman/kml/static/'+str(session['token']))
        return render_template("view.html",token=session['token'], number=10)
>>>>>>> 44ab447a10c683fcea2d59a9bb60946080fbd3ca

@app.route('/viewme/<number>')
def viewme(number=None):
    return render_template('view.html', number=number)

@app.route('/view')
def view():
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
