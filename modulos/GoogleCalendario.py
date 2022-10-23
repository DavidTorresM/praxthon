from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
from gcsa.recurrence import Recurrence, DAILY, SU, SA

from beautiful_date import Jan, Apr,Oct

from datetime import datetime
from gcsa.event import Event


from gcsa.recurrence import Recurrence, DAILY
from datetime import date, datetime
import os 


class GoogleCalendario(object):
	"""Libreria para sincronizar con el google calendar."""
	def __init__(self, email, credential_json=None):
		super(GoogleCalendario, self).__init__()
		self.email = email
		self.credential_json = credential_json
		self.calendar = GoogleCalendar(email)

	def leer_recordatorios(self):
		return [i for i in self.calendar]


	def hacer_evento(self, descripcion, fecha, localizacion=""):
		from datetime import datetime
		from gcsa.event import Event

		event = Event(
		    descripcion,
		    start=fecha,#datetime(2022, 10, 24, 10, 0),
		    location=localizacion
		)
		self.calendar.add_event(event)



if __name__=='__main__':
	mail = GoogleCalendario(os.getenv("CORREO_CALENDAR"))
	mail.hacer_evento("Evento test2", datetime(2022, 10, 24, 10, 0),"Oficina")
	print(mail.leer_recordatorios())
