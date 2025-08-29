Agente IA local con API y frontend web.

Montar una IA local a la que poder hacerle consultas mediante API para poder usarla en cualquier equipo doméstico, admite alimentarla con nuevos datos proporcionados mediante archivos de texto.

Funciona con equipos que solo dispongan de CPU, pero se recomienda para un mayor rendimiento y mejor UX equipos con GPUs compatibles con CUDA como las NVIDIA RTX o similares.

Las prestaciones del hardware en las que se han realizado las pruebas han sido un equipo portátil con 32Gb de RAM, procesador Intel i7 de 8 núcleos, GPU Nvidia GForce MX250 y disco sólido NVME de 1Tb.

- Instalar ollama y el modelo a utilizar:

    curl -fsSL https://ollama.com/install.sh | sh

- Ejecutar el modelo (si no existe se descarga automáticamente)

    ollama run modelo

- Modelos más utilizados:


llama3.2        2.0GB
codellama       3.8GB
mistral         4.4GB
deepseek-r1     4.7GB
gpt-oss        13.0GB


- Algunos comandos útiles de ollama:
    
  serve       Start ollama
  create      Create a model
  show        Show information for a model
  run         Run a model
  stop        Stop a running model
  pull        Pull a model from a registry
  push        Push a model to a registry
  list        List models
  ps          List running models
  cp          Copy a model
  rm          Remove a model
  help        Help about any command

- Situarnos en la capeta del proyecto.

- Crear y activar el entorno virtual:

    python3 -m venv venv
    source venv/bin/activate

- Instalar las depencias necesarias:

    pip install -r requirements.txt

- Importante indicar en el archivo chat_app_ollama.py el nombre del modelo a utilizar en la variable MODEL.

- Añadir en /docs_app los documentos que va a consultar la IA. Estarán en formato .txt o .md
- Ejecutar watcher_docs.py para actualizar los cambios en los documentos.
- Ejecutar server_final.py para poner en marcha el servidor web.

Acceder desde el navegador a localhost:8000 para ver el frontend, en caso de acceder desde otra ubicación, susituir localhost por la dirección IP del servidor o el dominio asignado.

Muy importante especificar el e el código de los archivos .py el prompt deseado para que la IA se comporte como deseamos con los usuarios que van a hacer uso de la misma. En caso contrario se comportará tal como venga el modelo de serie.

by @as_informatico
