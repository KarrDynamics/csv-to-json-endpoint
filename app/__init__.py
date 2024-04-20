from flask import Flask
import os

app = Flask(__name__)

# Set the absolute path to the templates directory
app.template_folder = os.path.abspath('templates')

from app import routes
