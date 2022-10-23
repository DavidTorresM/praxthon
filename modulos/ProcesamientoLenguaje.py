# Para usar GPT
import os
import openai
import webbrowser

import sys 

import requests as r
from bs4 import BeautifulSoup

from GoogleCalendario import GoogleCalendario

import time
from datetime import datetime
import hashlib


class ProcesamientoLenguaje(object):
	"""Realiza el reconocimiento de lenguaje natural de las cadenas insertadas"""
	def __init__(self, api_key_gpt3,model="text-davinci-002",temperature=0,top_p=1.0,frequency_penalty=0.0,resence_penalty=0.0):
		super(ProcesamientoLenguaje, self).__init__()
		self.api_key_gpt3 = api_key_gpt3
		self.model = model
		self.temperature = temperature
		self.top_p = top_p
		self.frequency_penalty = frequency_penalty
		self.resence_penalty = resence_penalty
	def preguntarIa(self,comando):
		openai.api_key = self.api_key_gpt3
		response = openai.Completion.create(
			model=self.model,
			prompt=f"{comando}",
			temperature=self.temperature,
			max_tokens=500,
			#top_p=self.top_p,
			#frequency_penalty=elf.frequency_penalty,
			#resence_penalty=self.resence_penalty
		)
		respuesta = [ i["text"] for i in response["choices"]]
		print("respuesta modelo",respuesta)
		return "\n".join(respuesta).lower()

	def preguntar_modo(self,oracion):
		respuesta = self.preguntarIa(f"¿Cual es el modo de la siguiente oracion?\n{oracion}")
		return respuesta
	def get_url_sitio(self,oracion):
		respuesta = self.preguntarIa(f"¿En la siguiente oracion estan hablando sobre sitios web, si la respuesta es si cual es la url del sitio?\n{oracion}")
		if respuesta.find("http") < 0:
			return None
		return respuesta[respuesta.find("http"):]
	def preguntar_ia_boolean(self,pregunta,oracion):
		respuesta = self.preguntarIa(f"{pregunta}\n{oracion}")
		return "sí" in respuesta
	def es_imperativa(self,oracion):
		respuesta = self.preguntarIa(f"¿en la siguiente oracion estan hablando en modo imperativo?\n{oracion}")
		return "sí" in respuesta
	def hablan_de_sitios_web(self,oracion):
		respuesta = self.preguntarIa(f"¿En la siguiente oracion estan hablando sobre sitios web?\n{oracion}")
		return "sí" in respuesta
	def checkBlackList(self,cadena,blackList):
		for b in blackList:
			if b in cadena:
				return True
		return False
	def alaisis_sentimiento(self,comando):
		openai.api_key = self.api_key_gpt3
		response = openai.Completion.create(
			model=self.model,
			prompt=f"{comando}",
			temperature=.3,
			max_tokens=60,
			top_p=1.0,
			frequency_penalty=0.5
		)
		respuesta = [ i["text"] for i in response["choices"]]
		print("respuesta modelo",respuesta)
		return "\n".join(respuesta).lower()

	def getHash(self):
		return hashlib.md5(datetime.now().__str__().encode("utf-8")).hexdigest()

	def mainProcesamiento(self,palabra):
		campo_semantico   = self.preguntarIa(f"cual es el campo semantico de la siguiente palabra \n {palabra}")
		resultado_bot     = self.preguntarIa(f"{palabra}")
		esImperativa = self.es_imperativa(palabra)
		"""
		if self.es_imperativa(palabra):
			if self.checkBlackList(campo_semantico, ["aviso","notificación","alarma", "nota", "recordatorio","calendar","calendario","calendar.google.com"]): # Recordatorios 
				if self.checkBlackList(campo_semantico,["calendar.google.com"]):
					url = campo_semantico.replace("\n","")
					webbrowser.open(url)
				else:
					pass




		elif campo_semantico in ["comunicación","emails"]:#Envio de correos electronicos
			pass

		"""

		if self.preguntar_ia_boolean("¿El siguiente texto es código fuente?\n",resultado_bot):
			md123 =  self.getHash()
			f = open(f"/tmp/sourceCode{md123}","w")
			f.write(resultado_bot)
			f.close()
			os.system(f"code /tmp/sourceCode{md123}")




	def get_fecha(self):
		page = r.get("http://www.fechadehoy.com/mexico")
		soup = BeautifulSoup(page.content, "html.parser")
		fecha = soup.find(id="fecha").text
		return fecha

if __name__=='__main__':
	nlp = ProcesamientoLenguaje(os.getenv("OPENAI_API_KEY"))
	#nlp.mainProcesamiento("¿que es un grafo bipartito en teoria de grafos?")
	#nlp.mainProcesamiento("Abre youtube y busca videos de gatitos")

	if sys.argv[1] == "1":
		nlp.mainProcesamiento(sys.argv[2])
	if sys.argv[1] == "2":
		nlp.alaisis_sentimiento(sys.argv[2])
	else:
		nlp.preguntarIa(sys.argv[2])

	
