from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
import uvicorn
import ollama
import os
from datetime import datetime
from chat_app_ollama import consultar_docs

app = FastAPI()

# Crear carpeta logs si no existe
os.makedirs("logs", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return FileResponse("static/index.html")

@app.post("/preguntar")
async def preguntar(request: Request):
    data = await request.json()
    pregunta = data.get("pregunta", "")

    prompt = f"""
    Responde SIEMPRE en español.
    Pregunta: {pregunta}
    """

    log_line = f"[{datetime.now()}] USER: {pregunta}\n"
    with open("logs/conversaciones.log", "a") as f:
        f.write(log_line)

    def stream_response():
        respuesta_completa = ""
        for chunk in ollama.chat(
            model="llama3.2",
            messages=[{"role": "user", "content": prompt}],
            stream=True
        ):
            if "message" in chunk and "content" in chunk["message"]:
                token = chunk["message"]["content"]
                respuesta_completa += token
                yield token
        # Guardamos la respuesta completa al final
        with open("logs/conversaciones.log", "a") as f:
            f.write(f"BOT: {respuesta_completa}\n\n")

    return StreamingResponse(stream_response(), media_type="text/plain")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

