import gradio as gr
from utils import process_csv, search_row_by_name, clean_Data, refresh_data1, refresh_data2, aniquilar

# Crear la interfaz de Gradio
with gr.Blocks(title="CALIFICAINATOR 3000") as Cass:
    gr.Markdown("CALIFICAINATOR 3000")

    with gr.Tab("Seleccion de datos"):
        file_input = gr.File(label="Cargar archivo CSV", type="filepath")
        pp_button = gr.Button("Procesar")
        tabla = gr.Dataframe()

        # Primera columna
        nombre_input = gr.Textbox(label="Nombre que contiene las respuestas correctas")
        multiple_respuestas_checkbox = gr.Checkbox(label="Múltiples respuestas")
        buscar_button = gr.Button("Buscar")

        # Segunda columna
        resultado_tabla = gr.Dataframe()
        confirmar_datos = gr.Button("Confirmar datos")
        gr.Text("Es todo por este paso, si esta de acuerdo con los resultados, pasar a la pestaña CALIFICAR", label="NOTA")

    with gr.Tab("CALIFICAR"):
        gr.Markdown("PULSA EL BOTON REFRESCAR Y VERIFICA QUE LOS DATOS SEAN CORRECTOS")
        with gr.Row():
            gr.Text("A la izquierda deberías ver el archivo con todas las respuestas de los estudiantes", label="NOTA")
            gr.Text("A la derecha deberías ver las respuestas correctas", label="NOTA")
        with gr.Row():
            TRespuestas = gr.Dataframe()
            TPatron = gr.Dataframe()
        with gr.Column():
            refresh1 = gr.Button("Refrescar")
        with gr.Row():
            iniciar_Calificar = gr.Button("Comenzar a calificar")
            estado = gr.Text("EstadoActual", label="Estado")
        with gr.Column(visible=True) as output_col:
            tabla_calificaciones = gr.Dataframe()
            refresh2 = gr.Button("Refrescar")

    with gr.Tab("RESULTADOS"):
        gr.Text("Pendiente", label="Pendiente")

    with gr.Accordion("Open for More!"):
        gr.Markdown("Look at me...")

    # Vincular los botones a las funciones
    pp_button.click(process_csv, inputs=file_input, outputs=tabla)
    buscar_button.click(search_row_by_name, inputs=[tabla, nombre_input], outputs=resultado_tabla)
    confirmar_datos.click(clean_Data, inputs=[nombre_input, resultado_tabla])
    refresh1.click(refresh_data1, outputs=[TRespuestas, TPatron])
    refresh2.click(refresh_data2, outputs=tabla_calificaciones)
    iniciar_Calificar.click(aniquilar)

if __name__ == "__main__":
    Cass.launch(debug=True,share=True)
