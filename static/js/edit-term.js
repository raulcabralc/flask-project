const termo = document.getElementById("termo");
const definicao = document.getElementById("definicao");
const counter = document.getElementById("counter");
const button = document.getElementById("button");

definicao.addEventListener("input", () => {
  counter.innerHTML = definicao.value.length;
});

putValues();

async function putValues() {
  try {
    await fetch(`/glossario/edit/${id}`, {
      method: "GET",
      headers: {
        "Content-type": "application/json",
      },
    });

    termo.value = termoValue;
    definicao.value = definicaoValue;
  } catch (e) {}
}
