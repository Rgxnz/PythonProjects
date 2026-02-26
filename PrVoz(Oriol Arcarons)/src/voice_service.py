import speech_recognition as sr

class VoiceService:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        self.mic = sr.Microphone()

    def capturar_frase(self):
        with self.mic as source:
            try:
                print(">>> Calibrando silencio...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                self.recognizer.energy_threshold += 10 
                
                print(">>> ¡HABLA YA!")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=8)
                
                print(">>> Procesando con Google IA...")
                resultado = self.recognizer.recognize_google(audio, language="es-ES", show_all=True)
                
                if not resultado or 'alternative' not in resultado:
                    return None, 0
                
                mejor_opcion = resultado['alternative'][0]
                texto = mejor_opcion['transcript'].lower()
                confianza = mejor_opcion.get('confidence', 0)
                
                return texto, confianza
                
            except sr.UnknownValueError:
                print(">>> La IA no entendió el audio.")
                return None, 0
            except Exception as e:
                print(f" >>> Error técnico: {e}")
                return None, 0