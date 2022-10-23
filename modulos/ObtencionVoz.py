import pyttsx3
import speech_recognition as sr
import webbrowser
import datetime
import pywhatkit
import os
import yfinance as yf
import pyjokes

ERROR_NO_ENTIENDO = "No te entiendo"
ERROR_NO_RESULTADOS = "No te entendi o no puedo encontrar resultados"
INFO_ESTOY_ESPERANDO = "Estoy esperando tus ordenes"


class ObtencionVoz(object):
	"""Modulo para obtener la información de voz"""
	def __init__(self, languaje_habla="spanish",lenguaje_reconocimiento="es-MX", tasa_muestreo=150,volume=1):
		super(ObtencionVoz, self).__init__()
		self.languaje_habla = languaje_habla
		self.tasa_muestreo = tasa_muestreo
		self.volume = volume
		self.lenguaje_reconocimiento = lenguaje_reconocimiento

	def speaking(self,message):
		engine = pyttsx3.init()
		engine.setProperty('rate', self.tasa_muestreo)
		engine.setProperty('voice', self.languaje_habla)
		engine.setProperty('volume', self.volume)
		engine.say(message)
		engine.runAndWait()

	def transform(self):
		r = sr.Recognizer()
		with sr.Microphone() as source:
			r.adjust_for_ambient_noise(source)
			r.pause_threshold = 0.8
			said = r.listen(source)
			try:
				q = r.recognize_google(said, language=self.lenguaje_reconocimiento)
				return q.strip()
			except sr.UnknownValueError:
				return ERROR_NO_ENTIENDO
			except sr.RequestError:
				return ERROR_NO_RESULTADOS
			except e:
				return INFO_ESTOY_ESPERANDO

if __name__=='__main__':

	voz_objeto = ObtencionVoz()
	voz_objeto.speaking("Esto es una prueba. Soy payton bot")
	print(voz_objeto.transform())




