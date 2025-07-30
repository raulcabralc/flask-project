from flask import Flask, render_template, request, url_for, redirect, jsonify
import os
import csv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from dotenv import load_dotenv
from markdown import markdown

app = Flask(__name__)

load_dotenv()
GEMINI_API_KEY = os.getenv("gemini_key")
if not GEMINI_API_KEY:
    raise ValueError("The GEMINI_API_KEY environment variable is not configured. Please, add it to your .env file.")

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=GEMINI_API_KEY)

# Store para histórico de conversas por sessão
store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# Novo template de prompt usando ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a programming assistant who teaches in English and helps people with Python difficulties; your answers should not be too long, without using symbols such as #, ``` or markdown; always use HTML tags: use <code> only to show complete code examples with the exact structure: (<br /><pre><code><div class="code"><span class="text">age</span> <span class="keyword">=</span> <span class="number">18</span><span class="keyword">if</span> <span class="text">age</span> <span class="keyword">>=</span> <span class="number">18</span><span class="text">:</span><span class="builtin">print</span><span class="text">(</span><span class="string">"Higher age"</span><span class="text">)</span><span class="keyword">elif</span> <span class="text">age</span> <span class="keyword">>=</span> <span class="number">16</span><span class="text">:</span> <span class="builtin">print</span><span class="text">(</span><span class="string">"Allowed to vote"</span><span class="text">)</span><span class="keyword">else</span><span class="text">:</span><span class="builtin">print</span><span class="text">(</span><span class="string">"Under age"</span><span class="text">)</span></div></code></pre><br />), without modifying a thing in this structure, it is important that the <br /> are placed in the start and end of the <div class="code">; when you mention terms like for, if, switch or methods such as enter, exit, use only <span class="code-example">palavra</span>; the use of <code> to highlight isolated terms is forbidden, instead, use <span class="code-example">; Watch out for code identation, it is incredibly important; The identation in the code examples are crucial;"""),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

# Criar a chain com histórico
chain = prompt | llm
genai = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

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
                    return jsonify({"error": "CSV line formatting is not correct"})
            else:
                return jsonify({"error": "ID not found"})
    
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

                return jsonify({"success": "Updated term"})

@app.route('/gemini', methods=['GET', 'POST'])
def gemini():
    if request.method == 'GET':
        return render_template("gemini.html")
    
    data = request.get_json()
    pergunta = data.get("message")
    
    if not pergunta:
        return jsonify({"error": "Please, enter a question."}), 400
    
    try:
        # Usar uma sessão padrão ou baseada no IP do usuário
        session_id = request.remote_addr or "default"
        
        response = genai.invoke(
            {"input": pergunta},
            config={"configurable": {"session_id": session_id}}
        )

        htmlResponse = markdown(response.content)
        
        return jsonify({"response": htmlResponse})
    
    except Exception as e:
        return jsonify({"error": f"Error processing question: {str(e)}"}), 500

@app.errorhandler(404)
def pageNotFound(error):
    return render_template("404.html", requestedUrl=request.url)

if __name__ == '__main__':
    app.run(debug=True)