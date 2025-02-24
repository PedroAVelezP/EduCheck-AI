import pandas as pd
import numpy as np
import unicodedata
import re
import os
from ollama_manager import start_ollama_thread
from lightrag.components.model_client import OllamaClient
from lightrag.core.generator import Generator
from lightrag.core.component import Component

def aniquilar():
    try:
        start_ollama_thread()
        patron = "Files/Respuestas_Patron.csv"
        respuestas = "Files/Respuestas_Pendientes.csv"
        
        # Validar si los archivos existen
        if not os.path.exists(patron) or not os.path.exists(respuestas):
            return "Error: Faltan los archivos de respuestas o el patrón de respuestas."

        datos1 = pd.read_csv(patron, header=None)
        datos2 = pd.read_csv(respuestas, header=None)

        rango = len(datos1.columns)
        output_file = "Files/Calificaciones.csv"

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
                
                # Crear cliente y llamada a SimpleQA
                model = {
                    "model_client": OllamaClient(),
                    "model_kwargs": {"model": "llama3.2"}
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
        return "Calificación completada."
    except Exception as e:
        return f"Error durante el proceso de calificación: {str(e)}"
