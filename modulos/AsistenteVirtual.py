



#from EnviadorEmails import EnviadorEmails
#from EnviadorWhatsaap import EnviadorWhatsaap
from GoogleCalendario import GoogleCalendario
from ObtencionVoz import ObtencionVoz
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

if __name__=='__main__':
	os.exit()
	if primeraVez():
		voz.speaking(f"Hola soy {NOMBRE_BOT} tu asistente personal.")
		voz.speaking("Voy a comenzar pidiendote algunos cuantos datos.")
		nombre = pedir_dato("nombre")
		email  = pedir_dato("Correo electronico")
		#Entrenar modelo
		voz.speaking("Vamos a empezar a hacer el reconocimiento facial.")
		voz.speaking("Se utilizara para que puedas acceder a tu cuenta.")
		voz.speaking("Para que pueda recordar bien tu rostro necesito que hagas diferentes gestos.")
		working_directory = face_recognition.prepare_working_directory(nombre)
		face_recognition.get_samples_faces_from_cam(working_directory[1])
		
		hilo1 = threading.Thread(target=voz.speaking,args=("Estoy recordando tu rostro espera un momento",))
		hilo1.start()
		face_recognition.train_model(working_directory)
		voz.speaking("Listo ya recorde tu rostro.")
	else:
		#nombre = pedir_dato("nombre").lower()
		nombre = input()
		#voz.speaking("Vere tu cara para que podamos iniciar sessión.")
		working_directory = face_recognition.prepare_working_directory(nombre)
		es_quien_dice_ser = face_recognition.reconocimiento_facial(working_directory)
		if not es_quien_dice_ser:
			voz.speaking(f"Parece no eres {nombre}.")
			return None
		#voz.speaking("Vere tu cara para que podamos iniciar sessión.")
		voz.speaking(f"Hola {nombre} bienvenido. ¿En que'puedo ayudarte?")

		while True:
			input_usuario = voz.transform()
			if input_usuario in [voz.ERROR_NO_ENTIENDO,voz.ERROR_NO_RESULTADOS,voz.INFO_ESTOY_ESPERANDO]:
				respuesta_bot = procesar_lenguaje.mainProcesamiento(input_usuario)
				voz.speaking(respuesta_bot)









