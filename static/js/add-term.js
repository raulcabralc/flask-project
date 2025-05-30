const termo = document.getElementById("termo");
const definicao = document.getElementById("definicao");
const counter = document.getElementById("counter");
const button = document.getElementById("button");

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

class ValidateForm {
  constructor() {
    this.termo = termo;
    this.definicao = definicao;
    this.button = button;
    this.events();
  }

  events() {
    this.button.addEventListener("click", (e) => {
      this.handleSubmit(e);
    });
  }

  async handleSubmit(e) {
    e.preventDefault();

    const validFields = this.validFields();

    if (!validFields) return;

    await fetch("/glossario/adicionar", {
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
