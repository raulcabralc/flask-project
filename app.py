from flask import Flask, render_template, request, url_for, redirect, jsonify
import os
import csv
import google.generativeai as genai
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
# Carrega as variáveis de ambiente do arquivo .env
GEMINI_API_KEY = os.getenv("gemini_key")
if not GEMINI_API_KEY:
    raise ValueError("A variável de ambiente GEMINI_API_KEY não está configurada. Por favor, adicione-a ao seu arquivo .env")

# Configure the Gemini API
genai.configure(api_key=GEMINI_API_KEY)

@app.route('/')
def principal():
    return render_template('index.html')

@app.route('/equipe')
def sobre_a_equipe():
    return render_template('sobre.html')

@app.route('/glossario')
def glossario():
    glossario_de_termos = []
    
    try:
        with open('bd_glossario.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for t in reader:
                glossario_de_termos.append(t)
    except FileNotFoundError:
        # If file doesn't exist, create an empty one
        with open('bd_glossario.csv', 'w', newline='', encoding='utf-8') as csvfile:
            pass
    
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
        writer.writerow([termo, definicao])
    
    return redirect(url_for('glossario'))

@app.route('/gemini', methods=['GET', 'POST'])
def gemini():
    if request.method == 'GET':
        return render_template("gemini.html")
    
    pergunta = request.form.get("user-input")
    
    if not pergunta:
        return render_template("gemini.html", error="Por favor, insira uma pergunta.")
    
    try:
        # Create the generative model
        model = genai.GenerativeModel('gemini-pro')
        
        # Generate content
        response = model.generate_content(pergunta)
        
        return render_template("gemini.html", response=response.text)
    
    except Exception as e:
        return render_template("gemini.html", error=f"Erro ao processar pergunta: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)