import cv2
import numpy as np

class CameraUtils:
    @staticmethod
    def detectar_rostro(imagen):
        """Detecta el rostro usando Haarcascades[cite: 114]."""
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        rostros = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(rostros) > 0:
            (x, y, w, h) = rostros[0]
            rostro_recortado = gray[y:y+h, x:x+w]
            return True, rostro_recortado, (x, y, w, h)
        return False, None, None

    @staticmethod
    def convertir_a_bytes(imagen):
        """Convierte imagen a bytes para almacenamiento BLOB[cite: 67, 121]."""
        success, buffer = cv2.imencode('.jpg', imagen)
        return buffer.tobytes() if success else None

    @staticmethod
    def entrenar_y_predecir(lista_usuarios, foto_actual):
        """Entrenamiento en RAM y predicción[cite: 126, 127]."""
        # Se requiere opencv-contrib-python
        try:
            # Primero detectar el rostro en la imagen actual
            exito, rostro_actual, coords = CameraUtils.detectar_rostro(foto_actual)
            if not exito or rostro_actual is None:
                print("[CameraUtils] No se detectó rostro en la imagen actual")
                return "Desconocido"
            
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            
            rostros_entrenamiento = []
            ids = []
            nombres = {}

            for i, usuario in enumerate(lista_usuarios):
                # usuario[0]: id, usuario[1]: nombre, usuario[3]: cara_bytes
                # Convertimos los bytes de la BD de nuevo a imagen 
                nparr = np.frombuffer(usuario[3], np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
                
                if img is None:
                    print(f"[CameraUtils] Error decodificando imagen de usuario {usuario[1]}")
                    continue
                    
                rostros_entrenamiento.append(img)
                ids.append(i) # LBPH necesita IDs enteros
                nombres[i] = usuario[1]

            if not rostros_entrenamiento:
                print("[CameraUtils] Sin usuarios de entrenamiento válidos")
                return "Desconocido"

            recognizer.train(rostros_entrenamiento, np.array(ids))
            
            # Usar el rostro detectado, no toda la imagen
            id_predicho, confianza = recognizer.predict(rostro_actual)
            
            print(f"[CameraUtils] Predicción: ID={id_predicho}, Confianza={confianza:.2f}")
            
            # Umbral ajustado: menor confianza = mejor match en LBPH
            # Valores típicos: 0-50 es muy confiado, 50-100 es moderado, >100 es desconocido
            if confianza < 100 and id_predicho in nombres:
                return nombres[id_predicho]
            return "Desconocido"
        except Exception as e:
            print(f"[CameraUtils] Error en entrenar_y_predecir: {e}")
            return "Desconocido"