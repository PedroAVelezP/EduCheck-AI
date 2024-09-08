import os
import subprocess
import threading

def ollama():
    os.environ['OLLAMA_HOST'] = '0.0.0.0:11434'
    os.environ['OLLAMA_ORIGINS'] = '*'
    subprocess.Popen(["ollama", "serve"])

def start_ollama_thread():
    ollama_thread = threading.Thread(target=ollama)
    ollama_thread.start()
