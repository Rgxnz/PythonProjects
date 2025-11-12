import tkinter as tk
from tkinter import scrolledtext
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

load_dotenv()

API_KEY = os.getenv('API_KEY')
if not API_KEY:
    raise ValueError("No se encontró la API_KEY en las variables de entorno")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-2.5-flash')

contexto_panaderia = """
Eres un asistente virtual para la "Panadería". 
Responde amablemente a las preguntas de los clientes sobre nuestros productos y servicios.

INFORMACIÓN DE LA PANADERÍA:

PRODUCTOS Y PRECIOS:
- Pan blanco: $2.50
- Pan integral: $3.00
- Croissants: $1.50 cada uno
- Donuts: $2.00 cada uno
- Pastel de chocolate (porción): $4.50
- Pastel de vainilla (porción): $4.00
- Galletas variadas: $0.50 cada una
- Pan de ajo: $4.00
- Empanadas (carne/pollo/queso): $3.50 cada una
- Torta completa (8 porciones): $25.00-$35.00 según sabor
- Café: $1.50
- Té: $1.00
- Jugos naturales: $3.00

SERVICIOS ESPECIALES:
- Pedidos para eventos (mínimo 48 horas de anticipación)
- Tortas personalizadas para cumpleaños y bodas
- Canastas de desayuno
- Catering para empresas

HORARIO DE ATENCIÓN:
- Lunes a Viernes: 6:00 AM - 8:00 PM
- Sábado: 6:00 AM - 6:00 PM
- Domingo: 7:00 AM - 2:00 PM

PROMOCIONES ACTUALES:
- Desayuno ejecutivo: Café + 2 croissants = $4.00
- Combo familiar: 2 panes + 1 torta + 6 donuts = $15.00
- Martes de empanadas: 3x$9.00

MÉTODOS DE PAGO:
- Efectivo
- Tarjetas de crédito/débito
- Transferencia bancaria

INFORMACIÓN ADICIONAL:
- No se necesita reserva para la mayoría de productos
- Pedidos especiales requieren 48 horas de anticipación
- Ofrecemos servicio de entrega a domicilio (costo adicional según zona)
- Estacionamiento gratuito para clientes

Responde siempre de manera amable y profesional, proporcionando información clara y útil.
"""

def consultar_gemini(pregunta):
    """Consulta a la API de Gemini con el contexto de la panadería"""
    try:
        prompt = f"{contexto_panaderia}\n\nCliente: {pregunta}\nAsistente:"
        
        response = model.generate_content(prompt)
        
        if hasattr(response, 'text'):
            return response.text
        else:
            response_json = json.loads(response.text)
            return response_json.get('text', 'Lo siento, no pude procesar tu pregunta.')
            
    except Exception as e:
        return f"Error al consultar la API: {str(e)}"

def enviar_pregunta():
    """Función para enviar la pregunta y mostrar la respuesta"""
    pregunta = entrada_pregunta.get()
    if pregunta.strip():

        conversacion.config(state=tk.NORMAL)
        conversacion.insert(tk.END, f"Tú: {pregunta}\n", "usuario")
        conversacion.see(tk.END)
        

        respuesta = consultar_gemini(pregunta)
        

        conversacion.insert(tk.END, f"Asistente: {respuesta}\n\n", "asistente")
        conversacion.see(tk.END)
        conversacion.config(state=tk.DISABLED)
        

        entrada_pregunta.delete(0, tk.END)

def limpiar_conversacion():
    """Limpiar la conversación"""
    conversacion.config(state=tk.NORMAL)
    conversacion.delete(1.0, tk.END)
    conversacion.config(state=tk.DISABLED)

root = tk.Tk()
root.title("Asistente Virtual - Panadería Dulce Hogar")
root.geometry("600x500")
root.configure(bg="#FFF8E1")

titulo = tk.Label(root, 
                 text="Asistente Virtual - Panadería", 
                 font=("Arial", 16, "bold"),
                 bg="#8D6E63",
                 fg="white",
                 pady=10)
titulo.pack(fill=tk.X)

frame_conversacion = tk.Frame(root, bg="#FFF8E1")
frame_conversacion.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

conversacion = scrolledtext.ScrolledText(frame_conversacion,
                                        wrap=tk.WORD,
                                        width=70,
                                        height=20,
                                        font=("Arial", 10),
                                        bg="#FAFAFA")
conversacion.pack(fill=tk.BOTH, expand=True)

conversacion.tag_config("usuario", foreground="#1565C0", font=("Arial", 10, "bold"))
conversacion.tag_config("asistente", foreground="#2E7D32", font=("Arial", 10))

conversacion.insert(tk.END, 
                   "Bienvenido a Panadería Dulce Hogar. ¿En qué puedo ayudarte hoy?\n\n", 
                   "asistente")
conversacion.config(state=tk.DISABLED)

frame_entrada = tk.Frame(root, bg="#FFF8E1")
frame_entrada.pack(padx=10, pady=10, fill=tk.X)

label_pregunta = tk.Label(frame_entrada, 
                         text="Tu pregunta:", 
                         bg="#FFF8E1",
                         font=("Arial", 10))
label_pregunta.pack(anchor=tk.W)

entrada_pregunta = tk.Entry(frame_entrada, 
                           font=("Arial", 12),
                           width=50)
entrada_pregunta.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
entrada_pregunta.bind("<Return>", lambda event: enviar_pregunta())

frame_botones = tk.Frame(frame_entrada, bg="#FFF8E1")
frame_botones.pack(side=tk.RIGHT)

boton_enviar = tk.Button(frame_botones,
                        text="Enviar",
                        command=enviar_pregunta,
                        bg="#4CAF50",
                        fg="white",
                        font=("Arial", 10, "bold"),
                        padx=20)
boton_enviar.pack(side=tk.LEFT, padx=(0, 5))

boton_limpiar = tk.Button(frame_botones,
                         text="Limpiar",
                         command=limpiar_conversacion,
                         bg="#F44336",
                         fg="white",
                         font=("Arial", 10),
                         padx=15)
boton_limpiar.pack(side=tk.LEFT)

info_frame = tk.Frame(root, bg="#E8F5E8", relief=tk.RAISED, bd=1)
info_frame.pack(padx=10, pady=5, fill=tk.X)

info_label = tk.Label(info_frame,
                     text="💡 Pregunta por nuestros panes frescos, pasteles, promociones y horarios",
                     bg="#E8F5E8",
                     fg="#2E7D32",
                     font=("Arial", 9, "italic"),
                     pady=5)
info_label.pack()

root.mainloop()