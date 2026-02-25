import tkinter as tk
from tkinter import messagebox
from src.voice_service import VoiceService
from src.auth_dao import AuthDAO

class VoiceAuditApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VoiceAudit Login")
        self.service = VoiceService()
        self.dao = AuthDAO()

        # UI simplificada
        tk.Label(root, text="Nombre de Usuario:").pack(pady=5)
        self.ent_user = tk.Entry(root)
        self.ent_user.pack(pady=5)

        tk.Button(root, text="Iniciar Registro Vocal", command=self.proceso_registro).pack(pady=10)
        tk.Button(root, text="Consultar Auditoría", command=self.mostrar_auditoria).pack(pady=5)
        
        self.txt_logs = tk.Text(root, height=10, width=40)
        self.txt_logs.pack(pady=10)

    def proceso_registro(self):
        username = self.ent_user.get()
        if not username:
            messagebox.showwarning("Aviso", "Introduce un nombre")
            return

        # Captura mediante Facade 
        frase, confianza = self.service.capturar_frase()
        
        if frase:
            if messagebox.askyesno("Confirmación", f"¿Tu frase es: '{frase}'?"):
                # Datos variables para el JSONB 
                log_data = {"status": "OK", "confianza": confianza, "latencia": "1.1s"}
                if self.dao.registrar_usuario(username, frase, log_data):
                    messagebox.showinfo("Éxito", "Usuario registrado correctamente")
        else:
            messagebox.showerror("Error", "No se detectó voz clara")

    def mostrar_auditoria(self):
        logs = self.dao.obtener_auditoria_critica()
        self.txt_logs.delete(1.0, tk.END)
        for user, status in logs:
            self.txt_logs.insert(tk.END, f"ALERTA: {user} - Status: {status}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAuditApp(root)
    root.mainloop()