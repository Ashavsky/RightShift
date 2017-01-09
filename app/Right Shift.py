from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def search():
    # return render_template("landing.html")
    return render_template("search.html")

if __name__ == '__main__':
    app.run()
