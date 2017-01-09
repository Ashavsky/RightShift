# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
from contextlib import closing
import os

# configuration
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
DATABASE = os.path.join(PROJECT_ROOT, 'tmp', 'rightshift.db')
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def search():
    # return render_template("landing.html")
    return render_template("search.html")

@app.route('/admin')
def admin():
    # return render_template("landing.html")
    return render_template("admin.html")

@app.route('/add', methods=['POST'])
def add_entry():
    g.db.execute('insert into jobs (id, total_payment, location, hospital) values (?, ?, ?)',
                 [request.form['total_payment'], request.form['location'], request.form['hospital']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('admin'))

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('dbSchemaJobs.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run()
