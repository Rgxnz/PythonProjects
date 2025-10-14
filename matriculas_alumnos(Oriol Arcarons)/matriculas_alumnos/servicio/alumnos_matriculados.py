import os

class AlumnosMatriculados:
    ruta_archivo = "alumnos.txt"
    
    @staticmethod
    def matricular_alumno(alumno):
        """Añade un alumno al archivo de matrículas"""
        try:
            with open(AlumnosMatriculados.ruta_archivo, 'a', encoding='utf-8') as archivo:
                archivo.write(f"{alumno.nombre}\n")
            print(f"Alumno {alumno.nombre} matriculado correctamente.")
        except Exception as e:
            print(f"Error al matricular alumno: {e}")
    
    @staticmethod
    def listar_alumnos():
        """Lista todos los alumnos matriculados"""
        try:
            if not os.path.exists(AlumnosMatriculados.ruta_archivo):
                print("No hay alumnos matriculados.")
                return
            
            with open(AlumnosMatriculados.ruta_archivo, 'r', encoding='utf-8') as archivo:
                alumnos = archivo.readlines()
                
            if not alumnos:
                print("No hay alumnos matriculados.")
                return
                
            print("\n--- ALUMNOS MATRICULADOS ---")
            for i, alumno in enumerate(alumnos, 1):
                print(f"{i}. {alumno.strip()}")
            print("-----------------------------")
                
        except Exception as e:
            print(f"Error al listar alumnos: {e}")
    
    @staticmethod
    def eliminar_alumnos():
        """Elimina el archivo de alumnos"""
        try:
            if os.path.exists(AlumnosMatriculados.ruta_archivo):
                os.remove(AlumnosMatriculados.ruta_archivo)
                print("Archivo de alumnos eliminado correctamente.")
            else:
                print("No existe el archivo de alumnos.")
        except Exception as e:
            print(f"Error al eliminar archivo: {e}")