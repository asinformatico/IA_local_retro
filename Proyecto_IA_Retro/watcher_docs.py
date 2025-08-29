import os
import faiss
import pickle
import torch
from sentence_transformers import SentenceTransformer
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

DOCS_DIR = "docs_app"
INDEX_DIR = "vectorstore"
INDEX_FILE = os.path.join(INDEX_DIR, "faiss.index")
META_FILE = os.path.join(INDEX_DIR, "meta.pkl")

# Detectar dispositivo seguro
def get_safe_device():
    if torch.cuda.is_available():
        capability = torch.cuda.get_device_capability(0)
        print(f"⚡ GPU detectada: {torch.cuda.get_device_name(0)} con compute capability {capability}")
        # Requiere >= sm_70 para PyTorch 2.x
        if capability[0] >= 7:
            return "cuda"
        else:
            print("⚠️ GPU no compatible con esta versión de PyTorch. Usando CPU.")
    return "cpu"

device = get_safe_device()
model = SentenceTransformer("all-MiniLM-L6-v2", device=device)
print(f"✅ Modelo cargado en: {device}")

def build_vectorstore():
    os.makedirs(INDEX_DIR, exist_ok=True)
    textos, metadatos = [], []

    for fname in os.listdir(DOCS_DIR):
        if fname.endswith((".md", ".txt")):
            with open(os.path.join(DOCS_DIR, fname), "r", encoding="utf-8") as f:
                contenido = f.read()
                textos.append(contenido)
                metadatos.append({"archivo": fname})

    if not textos:
        print("⚠️ No se encontraron documentos en docs_app/")
        return

    embeddings = model.encode(textos, convert_to_numpy=True, show_progress_bar=True)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, INDEX_FILE)
    with open(META_FILE, "wb") as f:
        pickle.dump(metadatos, f)

    print(f"✅ Vectorstore actualizado con {len(textos)} documentos")

class DocsHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith((".md", ".txt")):
            print("🔄 Cambio detectado en documentación. Reconstruyendo índice...")
            build_vectorstore()

if __name__ == "__main__":
    build_vectorstore()
    observer = Observer()
    observer.schedule(DocsHandler(), DOCS_DIR, recursive=False)
    observer.start()
    print("👀 Watcher corriendo. Esperando cambios en docs_app/...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

