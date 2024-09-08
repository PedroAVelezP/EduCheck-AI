import pandas as pd
import numpy as np
import unicodedata
import re
from ollama_manager import start_ollama_thread
from lightrag.components.model_client import OllamaClient
from lightrag.core.generator import Generator
from lightrag.core.component import Component

# Procesar archivo CSV
def process_csv(file_contents):
    df = pd.read_csv(file_contents)
    df.to_csv("EduCheck-AI/Files/Respuestas_Pendientes.csv", index=False)
    return df

# Buscar fila por nombre
def search_row_by_name(df, name):
    selected_row = df[df.iloc[:, 1] == name]
    selected_row.to_csv("EduCheck-AI/Files/Respuestas_Patron.csv", index=False)
    return selected_row

# Limpiar datos y eliminar filas
def clean_Data(name, Patron_final):
    Patron_final.to_csv("EduCheck-AI/Files/Respuestas_Patron.csv", index=False)
    df_pendientes = pd.read_csv("EduCheck-AI/Files/Respuestas_Pendientes.csv")
    df_pendientes = df_pendientes[df_pendientes.iloc[:, 1] != name]
    df_pendientes.to_csv("EduCheck-AI/Files/Respuestas_Pendientes.csv", index=False)
    return df_pendientes

# Refrescar datos de Respuestas y Patrón
def refresh_data1():
    df1 = pd.read_csv("EduCheck-AI/Files/Respuestas_Pendientes.csv")
    df2 = pd.read_csv("EduCheck-AI/Files/Respuestas_Patron.csv")
    return df1, df2

# Refrescar datos de calificaciones
def refresh_data2():
    df3 = pd.read_csv("EduCheck-AI/Files/Calificaciones.csv")
    return df3

# Función de calificación
def aniquilar():
    start_ollama_thread()
    patron = "EduCheck-AI/Files/Respuestas_Patron.csv"
    respuestas = "EduCheck-AI/Files/Respuestas_Pendientes.csv"
    datos1 = pd.read_csv(patron, header=None)
    datos2 = pd.read_csv(respuestas, header=None)

    rango = len(datos1.columns)
    output_file = "EduCheck-AI/Files/Calificaciones.csv"

    columnas_calificaciones = ['Matricula', 'Nombre'] + [f'Pregunta {i}' for i in range(1, rango - 2)] + [f'Justificación {i}' for i in range(1, rango - 2)]
    filas = []

    def remove_accents(input_str):
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

    class SimpleQA(Component):
        def __init__(self, model_client: OllamaClient, model_kwargs: dict):
            super().__init__()
            self.generator = Generator(
                model_client=model_client,
                model_kwargs=model_kwargs,
                template=qa_template,
            )

        def call(self, input: dict) -> str:
            return self.generator.call({"input_str": str(input)})

        async def acall(self, input: dict) -> str:
            return await self.generator.acall({"input_str": str(input)})

    for h in range(1, len(datos2)):  # Iterar sobre las filas de Respuestas_Pendientes
        matricula = datos2.iloc[h, 2]  # Obtener la matrícula desde la columna 3
        nombre = datos2.iloc[h, 1]  # Obtener el nombre desde la columna 2
        calificaciones_preguntas = []
        justificaciones_preguntas = []

        for i in range(3, rango):
            PRE = datos1.iloc[0, i]
            RC = datos1.iloc[1, i]
            RE = datos2.iloc[h, i]

            qa_template = """<SYS>
            You are a helpful assistant. Your task is to evaluate student responses. Below, you will be provided with the following information: the question (PRE), the correct answer (RC), and the student's answer (RE). You should consider the correct answer (RC) as 100 on the grading scale. If the student's answer is completely wrong or if the student attempts to guess with a broad or vague response, you should assign a 0.

            Please grade the student's answer on a scale from 0 (Incorrect answer) to 100 (Identical or similar to the indicated answer) and explain the reason for your grade using the following format:

            ## Calificación: 0-100
            ## Justificación:

            Your assistance is greatly appreciated, and your accurate evaluation will help in providing better feedback to students. Thank you for your help!
            </SYS>
            User: {{input_str}}
            You:"""

            model = {
                    "model_client": OllamaClient(),
                    "model_kwargs": {"model": "llama3.1:8b"}
                }
            qa = SimpleQA(**model)
            Entrada = qa(f"""
                PRE: {PRE}
                RC: {RC}
                RE: {RE}
            """)
            respuesta_generada = Entrada.data

            print(respuesta_generada)

            calificacion_match = re.search(r'Calificación: (\d+)', respuesta_generada)
            justificacion_match = re.search(r'Justificación:\s*(.+)', respuesta_generada, re.DOTALL)


            if calificacion_match:
                calificacion = int(calificacion_match.group(1))
                calificaciones_preguntas.append(calificacion)

            if justificacion_match:
                justificacion = justificacion_match.group(1).strip()
                justificaciones_preguntas.append(justificacion)

        nueva_fila = [matricula, nombre] + calificaciones_preguntas + justificaciones_preguntas
        filas.append(nueva_fila)

        df_calificaciones = pd.DataFrame(filas, columns=columnas_calificaciones)
        df_calificaciones.to_csv(output_file, index=False)
    return
