# PythonSOS

## Estrutura do site

### Página Inicial

A página inicial explica o que é Python e demonstra exemplos, como:

- Estruturas de Seleção
- Estruturas de repetição
- Vetores e matrizes
- Funções e procedimentos
- Tratamentos de exceção

### Página Gemini

Uma página com o chatbot Gemini AI, ele foi instruído para responder questões direcionadas a Python e ajudar com dúvidas de código em Python.

### Página Equipe

A página da equipe contém os quatro integrantes do trabalho:

- Raul Cabral
- João Lucas
- Diego Hardman
- João Victor

### Página Glossário

Uma página que possui um glossário. Permite o usuário criar, visualizar, editar e apagar um termo junto a sua definição.

## Tecnologias

### Linguagens

- Python
- JavaScript
- HTML
- Scss

### Frameworks

- Flask
- Langchain

### Banco de Dados

- Arquivo CSV

## Integração do Gemini

- 1 - Criação da IA, carregando a chave
- 2 - Instruções para o comportamento da IA
- 3 - Sistema de memória da IA
- 4 - Montagem da IA completa, juntando seus componentes
- 5 - Rota para receber a pergunta do Front-End
- 6 - IA retorna a resposta para o Front-End

## Executando a Aplicação

- Tenha o Python instalado
- Tenha as dependências instaladas:

  > flask
  > langchain-google-genai
  > langchain-core
  > langchain-community
  > python-dotenv
  > markdown

- Executar o app.py

## Essenciais do app.py

- Implementação do Gemini AI
  > Criação e instruções
- Rotas da aplicação
  > Rotas estáticas do website
- Glossário com CRUD
  > Rotas do glossário para o CRUD
- Armazenamento em CSV
  > Guarda, edita e remove dados do arquivo CSV
