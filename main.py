import argparse
from default_interface import create_default_interface
from debug_interface import create_debug_interface

def main():
    # Crear un parser de argumentos
    parser = argparse.ArgumentParser(description="Sistema de calificación")
    
    # Añadir el argumento --preset para elegir entre default o debug
    parser.add_argument("--preset", choices=["default", "debug"], default="default",
                        help="Elige la interfaz a iniciar: 'default' para la interfaz principal, 'debug' para la interfaz de pruebas")
    
    # Parsear los argumentos
    args = parser.parse_args()

    # Elegir la interfaz según el valor de --preset
    if args.preset == 'default':
        print("Iniciando interfaz predeterminada...")
        app = create_default_interface()
    elif args.ppreset == 'debug':
        print("Iniciando interfaz de depuración...")
        app = create_debug_interface()

    # Lanzar la aplicación Gradio
    app.launch(debug=True, share=True)

if __name__ == "__main__":
    main()
