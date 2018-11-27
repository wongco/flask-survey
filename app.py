from flask import Flask, request, session, render_template, redirect, make_response
from surveys import surveys
from flask_debugtoolbar import DebugToolbarExtension
import json

app = Flask(__name__)
app.secret_key = "RANDOM KEY"

app.debug = True
debug = DebugToolbarExtension(app)


@app.route('/survey')
def start_survey():
    """displays selected survey info and intializes responses list"""

    sel_survey_name = "satisfaction"
    sel_survey = surveys[sel_survey_name]

    survey_title = sel_survey.title
    survey_instructions = sel_survey.instructions
    num_of_questions = len(sel_survey.questions)

    # intialize session key "answers" to empty list
    session['answers'] = []

    return render_template('survey.html', survey_title=survey_title, survey_instructions=survey_instructions, num_of_questions=num_of_questions)
