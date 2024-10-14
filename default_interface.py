import gradio as gr
from utils import process_csv, search_row_by_name, clean_Data, refresh_data1, refresh_data2, aniquilar

def create_default_interface():
    with gr.Blocks(title="CALIFICAINATOR 3000") as Cass:
        gr.Markdown("## CALIFICAINATOR 3000")

        with gr.Tab("Seleccion de datos"):
            # Inputs y botones para cargar datos
            file_input = gr.File(label="Cargar archivo CSV", type="filepath")
            pp_button = gr.Button("Procesar archivo")
            tabla = gr.Dataframe(headers=["Matricula", "Nombre", "Pregunta 1", "..."], label="Vista Previa CSV")

            nombre_input = gr.Textbox(label="Nombre que contiene las respuestas correctas", placeholder="Ingrese el nombre...")
            multiple_respuestas_checkbox = gr.Checkbox(label="Múltiples respuestas")
            buscar_button = gr.Button("Buscar")

            resultado_tabla = gr.Dataframe(headers=["Matricula", "Nombre", "Respuestas"], label="Respuestas Correctas")
            confirmar_datos = gr.Button("Confirmar datos")
            gr.Text("Si está de acuerdo con los resultados, pasa a la pestaña CALIFICAR.", label="Nota")

            # Asignar funcionalidad a los botones
            pp_button.click(process_csv, inputs=file_input, outputs=tabla)  # Procesar archivo CSV
            buscar_button.click(search_row_by_name, inputs=[tabla, nombre_input], outputs=resultado_tabla)  # Buscar fila
            confirmar_datos.click(clean_Data, inputs=[nombre_input, resultado_tabla])  # Confirmar y limpiar datos

        with gr.Tab("CALIFICAR"):
            gr.Markdown("### Verifica los datos antes de calificar:")
            with gr.Row():
                gr.Text("A la izquierda: Respuestas de los estudiantes", label="Nota")
                gr.Text("A la derecha: Respuestas correctas", label="Nota")
            with gr.Row():
                TRespuestas = gr.Dataframe(label="Respuestas estudiantes")
                TPatron = gr.Dataframe(label="Respuestas correctas")
            refresh1 = gr.Button("Refrescar datos")
            iniciar_Calificar = gr.Button("Comenzar a calificar")
            estado = gr.Text("Esperando acción...", label="Estado")
            tabla_calificaciones = gr.Dataframe()
            refresh2 = gr.Button("Actualizar calificaciones")

            # Asignar funcionalidad a los botones
            refresh1.click(refresh_data1, outputs=[TRespuestas, TPatron])  # Refrescar datos de respuestas y patrón
            refresh2.click(refresh_data2, outputs=tabla_calificaciones)  # Refrescar calificaciones
            iniciar_Calificar.click(aniquilar, outputs=estado)  # Comenzar a calificar

        with gr.Tab("RESULTADOS"):
            gr.Markdown("### Resultados finales")
            resultados_finales = gr.Dataframe(headers=["Matrícula", "Nombre", "Calificación"], label="Resultados Pendientes")
            refresh_resultados = gr.Button("Refrescar Resultados")

            # Asignar funcionalidad al botón de refrescar resultados
            refresh_resultados.click(refresh_data2, outputs=resultados_finales)

        return Cass
