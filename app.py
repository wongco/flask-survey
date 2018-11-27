from flask import Flask, request, session, render_template, redirect, make_response
from surveys import surveys
from flask_debugtoolbar import DebugToolbarExtension
import json

app = Flask(__name__)
app.secret_key = "RANDOM KEY"

app.debug = True
debug = DebugToolbarExtension(app)
