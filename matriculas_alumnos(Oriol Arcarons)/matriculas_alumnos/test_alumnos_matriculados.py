from dominio.alumno import Alumno
from servicio.alumnos_matriculados import AlumnosMatriculados

def mostrar_menu():
    print("\n=== SISTEMA DE MATRÍCULAS ===")
    print("1) Matricular alumno")
    print("2) Listar alumnos")
    print("3) Eliminar archivo de alumnos")
    print("4) Salir")
    print("==============================")

def main():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-4): ").strip()
        
        if opcion == "1":
            nombre = input("Ingrese el nombre del alumno: ").strip()
            if nombre:
                alumno = Alumno(nombre)
                AlumnosMatriculados.matricular_alumno(alumno)
            else:
                print("El nombre no puede estar vacío.")
                
        elif opcion == "2":
            AlumnosMatriculados.listar_alumnos()
            
        elif opcion == "3":
            confirmacion = input("¿Está seguro de que desea eliminar todos los alumnos? (s/n): ").strip().lower()
            if confirmacion == 's':
                AlumnosMatriculados.eliminar_alumnos()
            else:
                print("Operación cancelada.")
                
        elif opcion == "4":
            print("¡Hasta luego!")
            break
            
        else:
            print("Opción no válida. Por favor, seleccione 1-4.")

if __name__ == "__main__":
    main()