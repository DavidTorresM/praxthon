
import smtplib



class EnviadorEmails(object):
	"""Envia emails"""
	def __init__(self, email_user, password, email_send, subject,message):
		super(EnviadorEmails, self).__init__()
		self.email_user = email_user
		self.password = password
		self.email_send = email_send
		self.subject = subject
		self.message = message

	def send_email(self):
		# create smtp session 
		s = smtplib.SMTP('smtp.live.com', 587) 

		# start tls for security 
		s.starttls() 
		print("Envios")
		# authentication 
		s.login(self.email_user, self.email_send) 

		# message to be sent 
		message = self.message
		print("Envios")
		# sending the mail 
		s.sendmail(self.email_user, self.email_send, message) 
		print("Envios")
		# terminating the session 
		s.quit()


if __name__=='__main__':
	mail = EnviadorEmails()
	mail.send_email()
