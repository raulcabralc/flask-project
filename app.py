from flask import Flask, render_template, request, url_for, redirect, jsonify
import os
import csv
import google.generativeai as genai
from dotenv import load_dotenv
from markdown import markdown

app = Flask(__name__)

load_dotenv()
# Carrega as variáveis de ambiente do arquivo .env
GEMINI_API_KEY = os.getenv("gemini_key")
if not GEMINI_API_KEY:
    raise ValueError("A variável de ambiente GEMINI_API_KEY não está configurada. Por favor, adicione-a ao seu arquivo .env")

# Configure the Gemini API
genai.configure(api_key=GEMINI_API_KEY)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/equipe')
def equipe():
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

@app.route('/glossario/adicionar', methods=["GET", 'POST'])
def criar_termo():
    if request.method == "GET":
        return render_template("add-term.html")

    data = request.get_json()
    termo = data.get("termo")
    definicao = data.get("definicao")

    if os.path.exists('bd_glossario.csv') and os.path.getsize('bd_glossario.csv') > 0:
        with open('bd_glossario.csv', 'rb') as arquivo:
            arquivo.seek(-1, 2)
            ultimo_char = arquivo.read(1)
            
        if ultimo_char != b'\n':
            with open('bd_glossario.csv', 'a', encoding='UTF-8') as arquivo:
                arquivo.write('\n')
    
    with open('bd_glossario.csv', 'a', newline='', encoding='UTF-8') as arquivo:
        writer = csv.writer(arquivo, delimiter=';')
        writer.writerow([termo, definicao])

@app.route('/glossario/apagar/<id>')
def apagar_termo(id):
    with open('bd_glossario.csv', 'r', encoding='UTF-8') as arquivo:
        file = arquivo.read().split("\n")
        if file:
            newId = int(id) - 1
            file.pop(newId)
            fileJoined = "\n".join(file)
            with open("bd_glossario.csv", "w", encoding="UTF-8") as newFile:
                newFile.write(fileJoined)
    
    return redirect(url_for('glossario'))

@app.route("/glossario/editar/<id>", methods=["GET", "POST"])
def editar_termo(id):

    if request.method == "GET":
        with open('bd_glossario.csv', 'r', encoding='UTF-8') as arquivo:
            reader = csv.reader(arquivo, delimiter=';')
            linhas = list(reader)

            if 1 <= int(id) <= len(linhas):
                linha_selecionada = linhas[int(id) - 1]
                
                if len(linha_selecionada) >= 2:
                    termo = linha_selecionada[0]
                    definicao = linha_selecionada[1]

                    if request.headers.get('Content-type') == 'application/json':
                        return jsonify({"termo": termo, "definicao": definicao})
                    
                    return render_template("edit-term.html", termo=termo, definicao=definicao, id=id)
                
                else:
                    return jsonify({"error": "Linha do CSV mal formatada"})
            else:
                return jsonify({"error": "ID não encontrado"})
    
    if request.method == "POST":
        data = request.get_json()
        termoEdit = data.get("termo")
        definicaoEdit = data.get("definicao")

        with open('bd_glossario.csv', 'r', encoding='UTF-8') as arquivo:
            reader = csv.reader(arquivo, delimiter=';')
            linhas = list(reader)

            if 1 <= int(id) <= len(linhas):
                linhas[int(id) - 1] = [termoEdit, definicaoEdit]

                with open('bd_glossario.csv', 'w', newline="", encoding='UTF-8') as arquivo:
                    writer = csv.writer(arquivo, delimiter=";")
                    writer.writerows(linhas)

                return jsonify({"success": "Termo atualizado"})

@app.route('/gemini', methods=['GET', 'POST'])
def gemini():
    if request.method == 'GET':
        return render_template("gemini.html")
    
    data = request.get_json()
    pergunta = data.get("message")
    
    if not pergunta:
        return jsonify({"error": "Por favor, insira uma pergunta."}), 400
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash', system_instruction='Você é um assistente de programação que ensina em português brasileiro e ajuda pessoas com dificuldade em Python; suas respostas não devem ser muito longas, sem usar símbolos como #, ``` ou markdown; utilize sempre tags HTML: use <code> apenas para mostrar exemplos completos de código com a estrutura exata (<br /><pre><code><div class="code"><span class="text">idade</span> <span class="keyword">=</span> <span class="number">18</span><span class="keyword">if</span> <span class="text">idade</span> <span class="keyword">>=</span> <span class="number">18</span><span class="text">:</span><span class="builtin">print</span><span class="text">(</span><span class="string">"Maior de idade"</span><span class="text">)</span><span class="keyword">elif</span> <span class="text">idade</span> <span class="keyword">>=</span> <span class="number">16</span><span class="text">:</span> <span class="builtin">print</span><span class="text">(</span><span class="string">"Pode votar"</span><span class="text">)</span><span class="keyword">else</span><span class="text">:</span><span class="builtin">print</span><span class="text">(</span><span class="string">"Menor de idade"</span><span class="text">)</span></div></code></pre><br />), sem modificar nada dentro dessa estrutura, é importante que os <br /> sejam colocados no início e no final do <div class="code">; ao mencionar termos como for, if, switch ou métodos como enter, exit, use apenas <span class="code-example">palavra</span>; é proibido usar <code> para destacar termos isolados, use sempre <span class="code-example">; Atente-se na identação do código, ela é de extrema importância; A identação nos exemplos de código são cruciais;')
        
        response = model.generate_content(pergunta)

        htmlResponse = markdown(response.text)
        
        return jsonify({"response": htmlResponse})
    
    except Exception as e:
        return jsonify({"error": f"Erro ao processar pergunta: {str(e)}"}), 500

@app.errorhandler(404)
def pageNotFound(error):
    return render_template("404.html", requestedUrl=request.url)

if __name__ == '__main__':
    app.run(debug=True)