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

@app.route('/admin/addjob')
def addjob():
    return render_template("addjob.html")

@app.route('/add', methods=['POST'])
def add_entry():
    payment = request.form['total_payment']
    location = request.form['location']
    hospital = request.form['hospital']
    job_title = request.form['job_title']
    g.db.execute('insert into jobs (job_title, total_payment, location, hospital) values (?, ?, ?, ?)',
                 [job_title, payment, location, hospital])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('admin'))

@app.route('/admin/showjobs')
def show_jobs():
    cur = g.db.execute('select job_title, total_payment, location, hospital from jobs order by id desc')
    jobs = [dict(job_title = row[0], total_payment=row[1], location=row[2], hospital = row[3]) for row in cur.fetchall()]
    return render_template('show_jobs.html', jobs=jobs)


@app.route('/clearjobs')
def clear_jobs():
    init_db()
    return redirect(url_for('admin'))

@app.route('/adddummyjobs')
def add_dumy_jobs():
    g.db.execute('insert into jobs (job_title, total_payment, location, hospital) values (?, ?, ?, ?)',
                 ["Resident Nurse", "$10,000.00", "San Deigo, California", "San Deigo Med"])
    g.db.execute('insert into jobs (job_title, total_payment, location, hospital) values (?, ?, ?, ?)',
                 ["P/T Physician", "$6,000.00", "Annaheim, California", "Avalanch Medical"])
    g.db.execute('insert into jobs (job_title, total_payment, location, hospital) values (?, ?, ?, ?)',
                 ["Nurse Manager", "$15,000.00", "Palo Alto, California", "Stanford Hospital"])
    g.db.commit()
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
