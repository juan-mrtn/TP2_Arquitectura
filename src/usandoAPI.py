import requests
import readline
import json

last_query = ""

def send_to_llama(user_query):
    """
    Envía el prompt al modelo llama3 usando la API local de Ollama y devuelve la respuesta.
    """
    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "llama3",
                "messages": [
                    {"role": "system", "content": "Sos un asistente útil."},
                    {"role": "user", "content": user_query}
                ]
            },
            stream=True
        )

        full_response = ""
        if response.status_code == 200:
            print("Conexión exitosa con LLaMA.")
        for line in response.iter_lines():
            if line:
                parsed = json.loads(line.decode("utf-8"))
                if "message" in parsed and "content" in parsed["message"]:
                    full_response += parsed["message"]["content"]

        return full_response or "[No se recibió respuesta válida]"
    except Exception as e:
        return f"[ERROR al invocar a LLaMA]: {e}"

def main():
    """
    Función principal que ejecuta el ciclo de conversación con el modelo.
    """
    global last_query
    print("Escribí tu consulta para LLaMA. Presioná Ctrl+C para salir.")
    try:
        while True:
            try:
                
                user_input = input("You: ")
                if user_input.strip() == "":
                    print("[Advertencia]: La consulta está vacía.")
                    continue

                last_query = user_input
                readline.add_history(user_input)

                print("Enviando a LLaMA...")
                response = send_to_llama(user_input)
                print(f"LLaMa: {response}\n")
            except Exception as e:
                print(f"[ERROR en el procesamiento de la consulta]: {e}")
    except KeyboardInterrupt:
        print("\n Programa finalizado por el usuario.")

if __name__ == "__main__":
    main()
