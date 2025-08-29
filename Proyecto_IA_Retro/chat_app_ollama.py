import os
import faiss
import pickle
import requests
import torch
from sentence_transformers import SentenceTransformer

INDEX_DIR = "vectorstore"
INDEX_FILE = os.path.join(INDEX_DIR, "faiss.index")
META_FILE = os.path.join(INDEX_DIR, "meta.pkl")

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"  # o llama2, codellama, etc.

def get_safe_device():
    if torch.cuda.is_available():
        capability = torch.cuda.get_device_capability(0)
        if capability[0] >= 7:  # GPUs con soporte oficial en PyTorch 2.x
            print(f"⚡ Usando GPU: {torch.cuda.get_device_name(0)}")
            return "cuda"
        else:
            print("⚠️ GPU detectada pero no soportada. Usando CPU.")
    return "cpu"

device = get_safe_device()
encoder = SentenceTransformer("all-MiniLM-L6-v2", device=device)
print(f"✅ Encoder cargado en: {device}")
def get_context(query, k=2):
    if not os.path.exists(INDEX_FILE):
        return "No hay documentación cargada todavía."

    index = faiss.read_index(INDEX_FILE)
    with open(META_FILE, "rb") as f:
        metadatos = pickle.load(f)

    q_emb = encoder.encode([query], convert_to_numpy=True)
    D, I = index.search(q_emb, k)
    contextos = []
    for idx in I[0]:
        if idx < len(metadatos):
            archivo = metadatos[idx]["archivo"]
            with open(os.path.join("docs_app", archivo), "r", encoding="utf-8") as f:
                contextos.append(f.read())
    return "\n\n".join(contextos)

def responder(pregunta):
    prompt = f"""
Responde siempre en idioma español.
Pregunta: {pregunta}
Respuesta:
"""
    resp = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    })
    data = resp.json()
    return data.get("response", "").strip()

def consultar_docs(query, k=2):
    return get_context(query, k)
