from logging import StrFormatStyle
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.get("/")
def show_survey_page():
    survey_title = survey.title
    survey_instructions = survey.instructions
    return render_template("survey_start.html",title=survey_title,instructions=survey_instructions )

@app.post("/begin")

def start_survey():
    return redirect("/questions/0")