



#from EnviadorEmails import EnviadorEmails
#from EnviadorWhatsaap import EnviadorWhatsaap
from GoogleCalendario import GoogleCalendario
from ObtencionVoz import ObtencionVoz,ERROR_NO_ENTIENDO,ERROR_NO_RESULTADOS,INFO_ESTOY_ESPERANDO
from ProcesamientoLenguaje import ProcesamientoLenguaje
from ReconocimientoFacial import ReconocimientoFacial

import os 
import threading

def primeraVez():
	dataPath = os.path.join(os.getcwd(),"primero")
	primera = os.path.exists(dataPath)
	if not primera:
		os.makedirs(dataPath)
		return True
	return False


NOMBRE_BOT = "payton bot"
email = ""
nombre = ""

def pedir_dato(dato):
	voz.speaking(f"¿Cual es tu {dato}?")
	input_voice = voz.transform()
	if dato=="nombre":
		respuesta_ia = procesar_lenguaje.preguntarIa(f"Obtener el nombre propio de la siguiente oracion \n {input_voice}. En caso de que nombre propio imprimir que no tiene").replace("\n"," ")
	else:
		respuesta_ia = procesar_lenguaje.preguntarIa(f"Obtener el {dato} de la siguiente oracion \n {input_voice}. En caso de que {dato} imprimir que no tiene").replace("\n"," ")
	if "no tiene" in respuesta_ia:
		voz.speaking(f"Parace que no has respondido tu {dato}. Puedes escribirlo en la terminal")
		respuesta = input(f"¿cual es tu {dato}?")
	else:
		respuesta = respuesta_ia
	return respuesta


voz = ObtencionVoz()
procesar_lenguaje = ProcesamientoLenguaje(os.getenv("OPENAI_API_KEY"))	
face_recognition = ReconocimientoFacial()
import time 


input_usuario = voz.transform()
print(f"Input usuario {input_usuario}")
if not input_usuario in [ERROR_NO_ENTIENDO,ERROR_NO_RESULTADOS,INFO_ESTOY_ESPERANDO]:
	respuesta_bot = procesar_lenguaje.mainProcesamiento(input_usuario)
	voz.speaking(respuesta_bot)











