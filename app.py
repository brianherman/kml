from flask import Flask, session, redirect, url_for, escape, request
from flask import render_template
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime, uuid

Base = declarative_base()

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

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    username = request.cookies.get('token')
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('/var/www/uploads/'+session['token']+'/upload.json')


@app.route('/view')
def view():
    username = request.cookies.get('token')
    big_file = '/var/www/uploads/'+session['token']+'/upload.json'
    
@app.route('/quit')
def quit():
    # remove the username from the session if it's there
    session.pop('token', None)
    return redirect(url_for('index'))

# set the secret key.  keep this really secret:
app.secret_key = 'm4jOOOS6ctRe6cnVzn9wMkd0AKN1xbkchPbUe8awq7Ykzw6eIDqFUGAxLN8Cw9BczAHqJ1KntzcffOSahyzMp3I0P26wS3G13i0BBNFB1cvriAZflMwMBcqgmPGz7s91gJdxI8oHq6WDS1861LfvqxlTEfG2OsNfyAnEdjXuHVqEHjkvRv5TCXg6GCCXdDSfQJrGYpPtA0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
