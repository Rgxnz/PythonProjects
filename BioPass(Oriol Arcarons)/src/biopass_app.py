import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
from src.usuario_dao import UsuarioDAO
from utils.camera_utils import CameraUtils

class BioPassApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BioPass DAO - Sistema Biométrico")
        self.root.geometry("700x600")
        
        self.dao = UsuarioDAO()
        self.cap = cv2.VideoCapture(0) 

        self.lbl_video = tk.Label(root) 
        self.lbl_video.pack(pady=10)

        self.lbl_nombre = tk.Label(root, text="Nombre del Usuario:", font=("Arial", 12))
        self.lbl_nombre.pack()
        self.ent_nombre = tk.Entry(root, font=("Arial", 12))
        self.ent_nombre.pack(pady=5)

        self.frame_botones = tk.Frame(root)
        self.frame_botones.pack(pady=20)

        self.btn_registrar = tk.Button(self.frame_botones, text="Registrar Rostro", command=self.ejecutar_registro, bg="blue", fg="white", width=20)
        self.btn_registrar.grid(row=0, column=0, padx=10)

        self.btn_login = tk.Button(self.frame_botones, text="Entrar (Login)", command=self.ejecutar_login, bg="green", fg="white", width=20)
        self.btn_login.grid(row=0, column=1, padx=10)

        self.actualizar_frame()

    def actualizar_frame(self):
        """Muestra el video de OpenCV en el Label de Tkinter."""
        ret, frame = self.cap.read()
        if ret:
            self.current_frame = frame 
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            img_tk = ImageTk.PhotoImage(image=img)
            
            self.lbl_video.configure(image=img_tk)
            self.lbl_video.image = img_tk
        
        self.root.after(15, self.actualizar_frame)

    def ejecutar_registro(self):
        nombre = self.ent_nombre.get()
        if not nombre:
            messagebox.showwarning("Error", "Introduce un nombre")
            return

        exito, rostro, coords = CameraUtils.detectar_rostro(self.current_frame)
        if exito:
            foto_bytes = CameraUtils.convertir_a_bytes(self.current_frame)
            cara_bytes = CameraUtils.convertir_a_bytes(rostro)
            
            self.dao.registrar_usuario(nombre, foto_bytes, cara_bytes)
            messagebox.showinfo("Éxito", f"Usuario {nombre} guardado en la BD.")
        else:
            messagebox.showerror("Error", "No se detecta rostro en el video.")

    def ejecutar_login(self):
        """Descarga usuarios, entrena en RAM y predice"""
        usuarios = self.dao.obtener_todos()
        if not usuarios:
            messagebox.showwarning("Error", "Base de datos vacía.")
            return

        nombre = CameraUtils.entrenar_y_predecir(usuarios, self.current_frame)
        if nombre != "Desconocido":
            messagebox.showinfo("Bienvenido", f"Acceso concedido a: {nombre}")
        else:
            messagebox.showwarning("Denegado", "Usuario no reconocido.")

    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()

if __name__ == "__main__":
    root = tk.Tk()
    app = BioPassApp(root)
    root.mainloop()