document.getElementById("searchbox").style.display = "block";

const tokenize = (value) => {
  value = value
    .toLowerCase()
    .replace(/\n/g, " ")
    .replace(/[?!;@#$%&]/g, " $& ")
    .replace(/[\]\[\(\)\{\}<>]/g, " $& ")
    .replace(/('s|'m|'d|'ll|'re|'ve|n't) /gi, " $1 ")
    .replace(/\. /g, " . ")
    .replace(/['’] /g, " ' ")
    .replace(/["“”]/g, " '' ");
  value = value
    .replaceAll("esp32", "esp 32")
    .replaceAll("esp8266", "esp 8266")
    .replaceAll("dht22", "dht 22")
    .replaceAll("dht11", "dht 11")
    .replaceAll("b-parasite", "b parasite")
    .replaceAll("nfc/rfid", "nfc rfid")
    .replaceAll("fastled", "fast led")
    .replaceAll("neopixelbus", "neopixel bus")
    .replaceAll("neopixel", "neo pixel")
    .replaceAll("h-bridge", "h bridge")
    .replaceAll("rgbw", "rgb white")
    .replaceAll("rgbww", "rgb cold warm")
    .replaceAll("rgbct", "rgb temperature brightness")
    .replaceAll("cannot", "can not")
    .replaceAll("addressable", "addressed");
  return value.replace(/\s+/g, " ").trim().split(" ");
};
const embed = (tokens) => {
  let output = Array.from({ length: 25 }, () => 0);
  let total = 0;
  for (let token of tokens) {
    if (!glove[token]) {
      continue;
    }
    const { idf, values } = glove[token];

    for (let i = 0; i < values.length; i++) {
      output[i] += values[i] * idf;
    }
    total += idf;
  }

  if (total == 0) return null;
  return output.map((x) => x / total);
};
const cosine = (a, b) => {
  const a_norm = a.map((x) => x * x).reduce((a, b) => a + b);
  const b_norm = b.map((x) => x * x).reduce((a, b) => a + b);
  return (
    a.map((x, i) => x * b[i]).reduce((a, b) => a + b) /
    Math.sqrt(a_norm * b_norm)
  );
};

let glove = {};
let embeddings = [];
(async () => {
  const r = await fetch("/_static/glove-25d-reduced.txt");
  const data = await r.text();
  for (const x of data.split("\n")) {
    const [w, idf, ...values] = x.split(" ");
    glove[w] = {
      idf: parseFloat(idf),
      values: values.map((x) => parseFloat(x)),
    };
  }
})();
(async () => {
  const r = await fetch("/embedding-index.json");
  embeddings = await r.json();
})();

const input = document.querySelector("#searchbox input");
const output = document.querySelector("#searchbox .output");
output.style.display = "flex";
output.style.flexDirection = "column";

const item = (href, title) => {
  const a = document.createElement("a");
  a.href = href;
  a.innerText = title;
  a.style.background = "#101010";
  a.style.color = "#ececec";
  a.style.padding = "0.5rem";
  a.style.borderRadius = "1rem";
  a.style.marginTop = "0.5rem";
  return a;
};
input.addEventListener("input", () => {
  const tokens = tokenize(input.value);
  const embedding = embed(tokens);
  const results = embedding
    ? embeddings
        .map((x) => ({
          ...x,
          similarity: cosine(x.embedding, embedding),
        }))
        .sort((a, b) => b.similarity - a.similarity)
    : [];

  output.replaceChildren(
    ...results.slice(0, 3).map((x) => item(x.page, x.title))
  );
});
