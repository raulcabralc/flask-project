from flask import Flask, render_template, request, url_for, redirect
import os
import csv

app = Flask(__name__)

@app.route('/')

def principal():
    return render_template('index.html')

@app.route('/equipe')

def sobre_a_equipe():
    return render_template('sobre.html')

@app.route('/glossario')
def glossario():

    glossario_de_termos = []

    with open('bd_glossario.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for t in reader:
            glossario_de_termos.append(t)

    return render_template('glossario.html', glossario=glossario_de_termos)

@app.route('/novo_termo')

def novo_termo():
    return render_template('novo_termo.html')

@app.route('/criar_termo', methods=['POST'])

def criar_termo():

    termo = request.form['termo']
    definicao = request.form['definicao']

    with open('bd_glossario.csv', 'a', newline='', encoding='UTF-8') as arquivo:
        writer = csv.writer(arquivo, delimiter=';')
        writer.writerow([termo,definicao])

    return redirect(url_for('glossario'))


app.run()