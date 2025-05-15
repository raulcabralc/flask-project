from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')

def ola():
    return render_template('index.html')

@app.route('/sobre_a_equipe')

def tchau():
    return render_template('sobre.html')
app.run()