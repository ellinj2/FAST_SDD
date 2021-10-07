from flask import render_template
from __main__ import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods =['GET', 'POST'])
def login():
    return None

@app.route('/logout')
def logout():
    return None

@app.route('/register', methods =['GET', 'POST'])
def register():
    return None