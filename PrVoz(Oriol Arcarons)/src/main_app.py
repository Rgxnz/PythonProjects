import tkinter as tk
from tkinter import messagebox
from src.voice_service import VoiceService
from src.auth_dao import AuthDAO

class VoiceAuditApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VoiceAudit Pro")
        self.root.geometry("400x450")
        
        self.voice_service = VoiceService()
        self.dao = AuthDAO()

        tk.Label(root, text="SISTEMA BIOMÉTRICO", font=("Arial", 12, "bold")).pack(pady=20)
        tk.Label(root, text="Usuario:").pack()
        self.ent_user = tk.Entry(root)
        self.ent_user.pack(pady=5)

        tk.Button(root, text="REGISTRAR", command=self.handle_registro, bg="#D4E6F1", width=20).pack(pady=10)
        tk.Button(root, text="LOGIN", command=self.handle_login, bg="#D5F5E3", width=20).pack(pady=10)
        tk.Button(root, text="AUDITORÍA", command=self.handle_auditoria, width=20).pack(pady=20)

    def handle_registro(self):
        user = self.ent_user.get()
        frase, conf = self.voice_service.capturar_frase()
        if frase:
            if messagebox.askyesno("Confirmar", f"¿Has dicho: '{frase}'?"):
                if self.dao.registrar_usuario(user, frase, conf):
                    messagebox.showinfo("Éxito", "Usuario registrado")

    def handle_login(self):
        user = self.ent_user.get()
        if not user:
            return messagebox.showwarning("Aviso", "Introduce un nombre de usuario")
            
        # 1. El Facade (VoiceService) captura la voz
        frase, conf = self.voice_service.capturar_frase()
        
        if frase:
            # 2. Informamos al usuario de lo que la IA ha detectado
            messagebox.showinfo("Procesando Voz", f"IA ha detectado: '{frase}'\nConfianza: {conf:.2f}")
            
            # 3. Validamos mediante el DAO en PostgreSQL
            res = self.dao.validar_login(user, frase, conf)
            
            if res == "SUCCESS":
                messagebox.showinfo("Login", "¡Identidad confirmada!")
            elif res == "USER_LOCKED":
                messagebox.showerror("BLOQUEO", "Usuario bloqueado. Demasiados intentos fallidos.")
            else:
                # Si falla, el usuario ya sabe qué frase "entendió" el sistema
                messagebox.showwarning("Denegado", f"La frase '{frase}' no es correcta para este usuario.")
        else:
            messagebox.showerror("Error", "No se detectó audio inteligible.")

    def handle_auditoria(self):
        logs = self.dao.obtener_auditoria()
        reporte = "HISTORIAL (JSONB):\n"
        for l in logs:
            reporte += f"{l[0]} | {l[2]} | Conf: {l[3]}\n"
        messagebox.showinfo("Auditoría", reporte if logs else "Vacío")

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAuditApp(root)
    root.mainloop()