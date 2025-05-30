const termo = document.getElementById("termo");
const definicao = document.getElementById("definicao");
const counter = document.getElementById("counter");
const button = document.getElementById("button");
const termoH1 = document.getElementById("termo-h1");

termo.addEventListener("input", () => {
  if (termo.classList.contains("error-field")) {
    termo.classList.remove("error-field");
    termo.nextSibling.remove();
  }
});

definicao.addEventListener("input", () => {
  counter.innerHTML = definicao.value.length;
  if (definicao.classList.contains("error-field")) {
    definicao.classList.remove("error-field");
    definicao.nextSibling.remove();
  }
});

const id = window.location.pathname.split("/").pop();

class ValidateForm {
  constructor() {
    this.termo = termo;
    this.definicao = definicao;
    this.button = button;
    this.events();
  }

  events() {
    this.putValues();
    this.button.addEventListener("click", (e) => {
      this.handleSubmit(e);
    });
  }

  async putValues() {
    try {
      const response = await fetch(`/glossario/editar/${id}`, {
        method: "GET",
        headers: {
          "Content-type": "application/json",
        },
      });

      if (response.ok) {
        const data = await response.json();
        termo.value = data.termo;
        definicao.value = data.definicao;

        termoH1.innerHTML = data.termo;

        counter.innerHTML = definicao.value.length;
      }
    } catch (e) {
      console.log("Erro!", e);
    }
  }

  async handleSubmit(e) {
    e.preventDefault();

    const validFields = this.validFields();

    if (!validFields) return;

    await fetch(`/glossario/editar/${id}`, {
      method: "POST",
      headers: {
        "Content-type": "application/json",
      },
      body: JSON.stringify({
        termo: termo.value,
        definicao: definicao.value,
      }),
    });

    window.location.pathname = "/glossario";
  }

  validFields() {
    let valid = true;

    for (let errorText of document.querySelectorAll(".error-text")) {
      errorText.remove();
    }

    for (let errorField of document.querySelectorAll(".error-field")) {
      errorField.classList.remove("error-field");
    }

    for (let field of document.querySelectorAll(".validate")) {
      if (!field.value.trim()) {
        valid = false;
        if (field.classList.contains("termo")) {
          this.createError(field, "Adicione o nome do termo");
        }

        if (field.classList.contains("definicao")) {
          this.createError(field, "Adicione uma definição para o termo");
        }
      }
    }

    return valid;
  }

  createError(field, message) {
    const div = document.createElement("div");
    div.innerHTML = message;
    div.classList.add("error-text");
    field.classList.add("error-field");
    field.insertAdjacentElement("afterend", div);
  }
}

const validate = new ValidateForm();
