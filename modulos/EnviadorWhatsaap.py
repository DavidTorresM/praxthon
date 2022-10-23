
import webbrowser

import pyautogui
import time 

class EnviadorWhatsaap(object):
	"""docstring for EnviadorWhatsaap"""
	def __init__(self, numero, mensaje):
		super(EnviadorWhatsaap, self).__init__()
		self.numero = numero
		self.mensaje = mensaje
	def enviar_mensaje(self):
		webbrowser.open(f'https://web.whatsapp.com/send?phone=+{self.numero}')
		time.sleep(10)
		pyautogui.typewrite(self.mensaje)
		pyautogui.press('enter')

if __name__=='__main__':
	mail = EnviadorWhatsaap("", "mensajito")
	mail.enviar_mensaje()
