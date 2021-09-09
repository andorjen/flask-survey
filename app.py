from logging import StrFormatStyle
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
#app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)



@app.get("/")
def show_survey_page():
    """Shows the survey start page with title and instructions"""
    session["responses"] = []
    survey_title = survey.title
    survey_instructions = survey.instructions
    return render_template("survey_start.html",title=survey_title,
        instructions=survey_instructions )

@app.post("/begin")
def start_survey():
    """Redirects to the first question when the user clicks Start"""
    session["current_question_number"] = 0
    return redirect("/questions/0")

@app.get("/questions/<int:question_number>")
def display_question(question_number):
    """Displays question"""

    question = survey.questions[question_number].question
    choices = survey.questions[question_number].choices
    return render_template("question.html", question = question, 
        choices = choices)

@app.post("/answer")
def record_answer_and_redirect():
    """take the answer from the submitted form,
    push it into session["responses"]
    and then redirect to the next question page
    """
    answer = request.form["answer"]
    responses = session["responses"]
    responses.append(answer)
    session["responses"] = responses
    current_question_number = session["current_question_number"] + 1
    session["current_question_number"] = current_question_number
    if current_question_number > len(survey.questions)-1:
        return render_template("completion.html")
    else:
        return redirect(f"/questions/{current_question_number}")