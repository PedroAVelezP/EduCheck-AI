import gradio as gr

def create_debug_interface():
    with gr.Blocks(title="DEBUG INTERFACE") as debug_interface:
        gr.Markdown("**Interfaz de depuración**")

        with gr.Tab("Pruebas"):
            gr.Markdown("Aquí puedes hacer pruebas adicionales.")
            gr.Textbox(label="Entrada de prueba")
            gr.Button("Procesar")

    return debug_interface
