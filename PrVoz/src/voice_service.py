import speech_recognition as sr

class VoiceService:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        # Ajustes de sensibilidad para ruido
        self.recognizer.dynamic_energy_threshold = True  # Ajuste continuo al ruido
        self.recognizer.pause_threshold = 0.8           # Segundos de silencio para terminar frase
        self.mic = sr.Microphone()

    def capturar_frase(self):
        """Gestiona el ciclo de vida del audio con filtrado de ruido avanzado"""
        with self.mic as source:
            print(">>> Calibrando ambiente... Silencio, por favor.")
            # Aumentamos la duración de la calibración (standard es 1s)
            self.recognizer.adjust_for_ambient_noise(source, duration=2) 
            
            # Ajustamos el factor de sensibilidad (más alto = menos sensible al ruido)
            self.recognizer.energy_threshold += 50 
            
            print(f">>> Umbral de energía actual: {self.recognizer.energy_threshold}")
            print(">>> Escuchando frase de paso...")
            
            try:
                # Limitamos el tiempo de escucha para evitar capturar ruido infinito
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10) 
                
                print(">>> Procesando señal acústica... ")
                # Traducción mediante motor externo 
                resultado = self.recognizer.recognize_google(audio, language="es-ES", show_all=True)
                
                if not resultado or 'alternative' not in resultado:
                    return None, 0
                
                mejor_opcion = resultado['alternative'][0]
                texto = mejor_opcion['transcript'].lower()
                confianza = mejor_opcion.get('confidence', 0)
                
                print(f">>> IA detectó: '{texto}' (Confianza: {confianza:.2f}) ")
                return texto, confianza
                
            except sr.WaitTimeoutError:
                print(">>> Error: No se detectó audio a tiempo.")
                return None, 0
            except Exception as e:
                print(f">>> Error en traducción: {e} ")
                return None, 0