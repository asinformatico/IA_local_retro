// ======= Utilidades de impresión tipo terminal =======
function createLine(text, type = "bot") {
  const chatBox = document.getElementById("chat-box");
  const line = document.createElement("div");
  line.className = `line ${type}`;
  const tag = document.createElement("span");
  tag.className = "tag";
  tag.textContent = type === "user" ? "[USER]" : "[BOT ]";
  const content = document.createElement("span");
  content.className = "content";
  content.textContent = text;
  line.appendChild(tag);
  line.appendChild(content);
  chatBox.appendChild(line);
  chatBox.scrollTop = chatBox.scrollHeight;
  return { line, content };
}

function updateStreamingLine(node, chunk) {
  node.textContent += chunk;
  const chatBox = document.getElementById("chat-box");
  chatBox.scrollTop = chatBox.scrollHeight;
}

function addError(text) {
  const chatBox = document.getElementById("chat-box");
  const line = document.createElement("div");
  line.className = "line error";
  line.textContent = `⚠ ${text}`;
  chatBox.appendChild(line);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// ======= Comando CLEAR / CLS =======
function checkClearCommand(cmd) {
  const normalized = cmd.toLowerCase();
  if (normalized === "clear" || normalized === "cls") {
    location.reload(); // recarga la página
    return true;
  }
  return false;
}

// ======= Web Audio API para efectos =======
const audioContext = new (window.AudioContext || window.webkitAudioContext)();

// Generar beep para teclas
function playBeep() {
  const osc = audioContext.createOscillator();
  const gain = audioContext.createGain();
  osc.type = "square";
  osc.frequency.setValueAtTime(880, audioContext.currentTime); // tono alto retro
  gain.gain.setValueAtTime(0.05, audioContext.currentTime);
  osc.connect(gain);
  gain.connect(audioContext.destination);
  osc.start();
  osc.stop(audioContext.currentTime + 0.05); // beep corto
}

// ======= Lógica de envío / streaming =======
async function enviarPregunta() {
  const input = document.getElementById("pregunta");
  const pregunta = input.value.trim();
  if (!pregunta) return;

  // Si es clear/cls => limpiar pantalla
  if (checkClearCommand(pregunta)) return;

  // Imprime entrada del usuario
  createLine(pregunta, "user");
  input.value = "";

  // Línea para el bot
  const { content } = createLine("", "bot");

  try {
    const response = await fetch("/preguntar", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ pregunta }),
    });

    if (!response.ok || !response.body) {
      throw new Error(`HTTP ${response.status}`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      const chunk = decoder.decode(value, { stream: true });
      updateStreamingLine(content, chunk);
    }
  } catch (err) {
    addError("Error al conectar con el servidor.");
  }
}

// ======= Eventos =======
document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("pregunta");
  const btn = document.getElementById("send-btn");

  input.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      enviarPregunta();
    } else {
      playBeep();
    }
  });

  btn.addEventListener("click", enviarPregunta);
});

