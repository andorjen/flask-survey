from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

RESPONSE_KEY = "responses"

@app.get("/")
def show_survey_page():
    """Shows the survey start page with title and instructions"""
    session[RESPONSE_KEY] = []

    return render_template("survey_start.html",
        survey = survey )

@app.post("/begin")
def start_survey():
    """Redirects to the first question when the user clicks Start"""
    session["current_question_number"] = 0 #refactor to use survey response length
    return redirect("/questions/0")

@app.get("/questions/<int:question_number>")
def display_question(question_number):
    """Displays question"""

    if len(session[RESPONSE_KEY]) != question_number:
        question_number = len(session[RESPONSE_KEY])
        flash("You're trying to access an invalid question")
        return redirect(f"/questions/{question_number}")

    if len(session[RESPONSE_KEY]) == len(survey.questions):
        return redirect("/thanks")

    question = survey.questions[question_number].question
    choices = survey.questions[question_number].choices
    return render_template("question.html", 
        question = question, 
        choices = choices) 

@app.post("/answer")
def record_answer_and_redirect():
    """take the answer from the submitted form,
    push it into session[RESPONSE_KEY]
    and then redirect to the next question page
    """
    answer = request.form["answer"]
    responses = session[RESPONSE_KEY]
    responses.append(answer)
    session[RESPONSE_KEY] = responses
    current_question_number = session["current_question_number"] + 1
    session["current_question_number"] = current_question_number
    if current_question_number > len(survey.questions)-1:
        return redirect("/thanks")
    else:
        return redirect(f"/questions/{current_question_number}")

@app.get("/thanks")
def display_thank_you():
    """Display thank you page at the end of the survey"""
    return render_template("completion.html")