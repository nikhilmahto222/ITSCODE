from flask import Flask, render_template, request, make_response, redirect,url_for
from owlready2 import *

app = Flask(__name__)

# Ontology Load
ontology = get_ontology("its.owl").load()

@app.route('/')
def home():
    firstName = request.cookies.get('firstName')

    if firstName:
            return redirect(url_for("home_panel"))
    return render_template("user.html")

@app.route('/user', methods=['GET', 'POST'])
def user():
    if request.method == 'POST':
        firstName = request.form['firstName']

        resp = make_response(redirect(url_for('home')))
        resp.set_cookie('firstName', firstName)

        user = ontology.Student(firstName)
        user.firstName.append(firstName)
        ontology.save("its.owl")

        return resp
    return render_template("user.html")

@app.route('/home')
def home_panel():

    firstName = request.cookies.get('firstName')
    return render_template('index.html', firstName = firstName)

@app.route('/calculate', methods=['POST'])
def area_calculation():
    if request.method == 'POST':
        base = int(request.form['base'])
        height = int(request.form['height'])
        
        area = 0.5 * base * height
        return render_template('result.html', area=area)

@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('home')))
    resp.set_cookie('firstName', '', expires=0)  # Clear the cookie
    return resp

if __name__ == "__main__":
    app.run(debug=True)