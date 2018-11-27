from flask import Flask, request, session, render_template, redirect, make_response
from surveys import surveys
from flask_debugtoolbar import DebugToolbarExtension
import json

app = Flask(__name__)
app.secret_key = "RANDOM KEY"

app.debug = True
debug = DebugToolbarExtension(app)


@app.route('/')
def select_survey():
    """ displays page with survey options """
    return render_template("select_survey.html", surveys=surveys)


@app.route('/selected_survey', methods=["POST"])
def save_survey():
    """ saves selected survey name to session and redirect to display survey view"""

    sel_survey_name = request.form.get("sel_survey_name")
    session['sel_survey_name'] = sel_survey_name
    return redirect('/survey')


@app.route('/survey')
def start_survey():
    """displays selected survey info and intializes responses list"""

    # Retreive selected survey name from session
    sel_survey_name = session['sel_survey_name']

    # Retreive selected survey instance
    sel_survey = surveys[sel_survey_name]

    survey_title = sel_survey.title
    survey_instructions = sel_survey.instructions
    total_questions = len(sel_survey.questions)

    # initialize current question in session to 1st
    session['current_question_num'] = 1
    # initialize session key "answers" to empty list
    session['answers'] = []

    return render_template('survey.html', survey_title=survey_title, survey_instructions=survey_instructions, total_questions=total_questions)


@app.route('/answer', methods=["POST"])
def save_answer():
    """Saves answer and redirects to GET display question page"""

    # retrieve answer submissions for question from HTML Form
    choice = request.form.get("choice")
    comment = request.form.get("comment")

    # if choice exists
    if choice:
        #  save to session
        answer_dict = {"choice": choice, "comment": comment}

        answers = session["answers"]
        answers.append(answer_dict)
        session["answers"] = answers

        # change session_current_question to +1
        session['current_question_num'] += 1

    question_url = f"/questions/{session['current_question_num']}"
    return redirect(question_url)


@app.route('/questions/<question_num>')
def question_form(question_num):
    """Obtains current question information and renders form"""

    # survey key name
    sel_survey_name = session['sel_survey_name']

    # survey instance
    sel_survey = surveys[sel_survey_name]

    question_num = int(question_num)

    # total question in current survey instance
    total_questions = len(sel_survey.questions)

    # if next question is unavailable, redirect to GET /thanks
    if question_num > total_questions:
        return redirect("/thanks")

    # index of question to render
    question_index = session['current_question_num'] - 1

    # current question instance in survey
    question = sel_survey.questions[question_index]

    return render_template(
        "question.html",
        question=question,
        question_num=question_num,
        total_questions=total_questions
    )


@app.route('/thanks')
def display_thanks():
    """ displays thank you page - end of survey """
    return render_template('thanks.html')
