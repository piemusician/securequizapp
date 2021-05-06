import os
from flask import Flask, url_for, render_template, request
from flask import redirect
from flask import session

app = Flask(__name__)

# In order to use "sessions",you need a "secret key".
# This is something random you generate.  
# For more info see: http://flask.pocoo.org/docs/0.10/quickstart/#sessions

app.secret_key=os.environ["SECRET_KEY"]; #This is an environment variable.  
                                     #The value should be set in Heroku (Settings->Config Vars).  
                                     #To run locally, set in env.sh and include that file in gitignore so the secret key is not made public.
def store_Answers(answer, x):
    if 'answer' + str(x) not in session:
        session['answer' + str(x)] = answer
    else:
        return render_template('page' + str(x) + '.html')

def my_Function(x, y):
    print(x + " " + y)
    
@app.route('/')
def renderMain():
    return render_template('home.html')

@app.route('/retakeQuiz')
def retakeQuiz():
    session.clear() #clears variable values and creates a new session
    return redirect(url_for('renderMain')) # url_for('renderMain') could be replaced with '/'

@app.route('/page1')
def renderPage1():
    return render_template('page1.html')

@app.route('/page2',methods=['GET','POST'])
def renderPage2():
    store_Answers(request.form['answer1'], 1)
    return render_template('page2.html')

@app.route('/page3',methods=['GET','POST'])
def renderPage3():
    store_Answers(request.form['answer2'], 2)
    return render_template('page3.html')

@app.route('/final', methods =['GET', 'POST'])
def renderFinal():
    score=0
    store_Answers(request.form['answer3'], 3)
    if session['answer1'] == 'Watches' or session['answer1'] == 'watches':
        score = score +1       
    if session['answer2'] == 'December 18, 2001' or session['answer2'] == '12/18/01':
        score = score +1
    if session['answer3'] == 'Ocean Eyes' or session['answer3'] == 'ocean eyes':
        score = score +1
    return render_template('final.html', finalScore=score)

if __name__=="__main__":
    app.run(debug=False)
