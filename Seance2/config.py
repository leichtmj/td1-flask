import os
from flask import Flask, render_template, render_template_string,request
from flask_sqlalchemy import SQLAlchemy

file_path = os.path.abspath(os.getcwd())+"/database/chinook.db"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)