import csv
import os

def detectar_encoding(archivo):
    """Intenta detectar la codificación del archivo"""
    encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'windows-1252']
    
    for encoding in encodings:
        try:
            with open(archivo, 'r', encoding=encoding) as file:
                file.read()
            return encoding
        except UnicodeDecodeError:
            continue
    
    return 'latin-1'  

def unificar_notas():

    archivo_uf1 = 'Notas_Alumnos_UF1.csv'
    archivo_uf2 = 'Notas_Alumnos_UF2.csv'
    archivo_salida = 'Notas_Alumnos.csv'
    
    try:

        encoding_uf1 = detectar_encoding(archivo_uf1)
        encoding_uf2 = detectar_encoding(archivo_uf2)
        
        print(f"Codificación detectada - UF1: {encoding_uf1}, UF2: {encoding_uf2}")
        

        datos_uf1 = {}
        with open(archivo_uf1, 'r', encoding=encoding_uf1) as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                id_alumno = row['Id']
                datos_uf1[id_alumno] = {
                    'Id': id_alumno,
                    'Apellidos': row['Apellidos'],
                    'Nombre': row['Nombre'],
                    'UF1': row['UF1']
                }
        

        datos_completos = []
        with open(archivo_uf2, 'r', encoding=encoding_uf2) as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                id_alumno = row['Id']
                if id_alumno in datos_uf1:
                    alumno = datos_uf1[id_alumno].copy()
                    alumno['UF2'] = row['UF2']
                    datos_completos.append(alumno)
        

        with open(archivo_salida, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['Id', 'Apellidos', 'Nombre', 'UF1', 'UF2']
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';')
            

            writer.writeheader()
            

            for alumno in datos_completos:
                writer.writerow(alumno)
        
        print(f"Archivo '{archivo_salida}' creado exitosamente con {len(datos_completos)} alumnos.")
        
    except FileNotFoundError as e:
        print(f"Error: No se pudo encontrar el archivo {e.filename}")
    except Exception as e:
        print(f"Ha ocurrido un error inesperado: {e}")


if __name__ == "__main__":
    unificar_notas()