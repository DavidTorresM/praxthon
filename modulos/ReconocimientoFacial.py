#imagenes 
import cv2
import os
import imutils
import numpy as np
#utilerias
import threading
import time
from datetime import datetime
import hashlib
import ObtencionVoz as obten


MUESTRAS_NUMERO = 300

class ReconocimientoFacial(object):
	"""Modulo para hacer el reconocimiento facial y la autenticación"""
	def __init__(self, numero_muestras=MUESTRAS_NUMERO):
		super(ReconocimientoFacial, self).__init__()
		self.voz = obten.ObtencionVoz()
		self.numero_muestras = numero_muestras

	def getHash(self):
		return hashlib.md5(datetime.now().__str__().encode("utf-8")).hexdigest()

	def prepare_working_directory(self,personName):
		""" Crea las carpetas para almacenar las imagenes del directorio."""
		dataPath = os.path.join(os.getcwd(),"data")
		personPath = os.path.join(dataPath,personName)
		if not os.path.exists(personPath):
			print('Carpeta creada: ',personPath)
			os.makedirs(personPath)
		return dataPath,personPath

	def get_samples_faces_from_cam(self,personPath):
		"""Realiza la toma de las capturas de la camara."""
		labels = ["seri@","sonriente","riendo","enojad@", "Guino un ojo","Guino el otro ojo","Hablando"]
		periodo = MUESTRAS_NUMERO//len(labels)
		index=0
		cap = cv2.VideoCapture(0)
		faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
		count = 0
		conta = 0 
		speak = True
		while True:
			ret, frame = cap.read()
			if ret == False: break
			frame =  imutils.resize(frame, width=640)
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			auxFrame = frame.copy()
			faces = faceClassif.detectMultiScale(gray,1.3,5)
			for (x,y,w,h) in faces:
				cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
				rostro = auxFrame[y:y+h,x:x+w]
				rostro = cv2.resize(rostro,(150,150),interpolation=cv2.INTER_CUBIC)
				cv2.imwrite(personPath + '/rotro_{}_{}.jpg'.format(self.getHash(),count),rostro)
				count = count + 1
				conta += 1
			if conta == periodo:
				index= (index+1)%(len(labels))
				conta = 0
				speak = True
			if speak:
				speak = False
				hilo1 = threading.Thread(target=self.voz.speaking,args=("Podrias poner tu cara "+labels[index],))
				hilo1.start()
				
			cv2.putText(frame,labels[index], (114,430), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)
			cv2.imshow('frame',frame)
			k = cv2.waitKey(1)
			if k == 27 or count >= MUESTRAS_NUMERO:
				break
		cap.release()
		cv2.destroyAllWindows() 

	def train_model(self,working_directory):
		dataPath = working_directory[0]
		personPath = working_directory[1]
		peopleList = [i for i in os.listdir(dataPath) if not i in [".Training",".Testing"]]
		print('Lista de personas: ', peopleList)
		labels = []
		facesData = []
		label = 0
		for nameDir in peopleList:
			personPath = dataPath + '/' + nameDir
			#print('Leyendo las imágenes')
			for fileName in os.listdir(personPath):
				#print('Rostros: ', nameDir + '/' + fileName)
				labels.append(label)
				facesData.append(cv2.imread(personPath+'/'+fileName,0))
				#image = cv2.imread(personPath+'/'+fileName,0)
				#cv2.imshow('image',image)
				#cv2.waitKey(10)
			label = label + 1

		#face_recognizer = cv2.face.EigenFaceRecognizer_create()
		#face_recognizer = cv2.face.FisherFaceRecognizer_create()
		face_recognizer = cv2.face.LBPHFaceRecognizer_create()
		print("Entrenando...")
		face_recognizer.train(facesData, np.array(labels))
		face_recognizer.write('modeloLBPHFace.xml')
		print("Modelo almacenado...")

	def reconocimiento_facial(self,working_directory):
		UMBRAL_MATCHES_POSITIVOS = 20; contador_p = 0; 
		UMBRAL_MATCHES_NEGATIVOS = 40; contador_n = 0; 
		dataPath = working_directory[0]
		personPath = working_directory[1]
		imagePaths = [i for i in os.listdir(dataPath) if not i in [".Training",".Testing"]]
		print('imagePaths=',imagePaths)
		#face_recognizer = cv2.face.EigenFaceRecognizer_create()
		#face_recognizer = cv2.face.FisherFaceRecognizer_create()
		face_recognizer = cv2.face.LBPHFaceRecognizer_create()
		# Leyendo el modelo
		#face_recognizer.read('modeloEigenFace.xml')
		#face_recognizer.read('modeloFisherFace.xml')
		face_recognizer.read('modeloLBPHFace.xml')
		cap = cv2.VideoCapture(0)
		#cap = cv2.VideoCapture('Video.mp4')

		faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
		while True:
			ret,frame = cap.read()
			if ret == False: break
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			auxFrame = gray.copy()
			faces = faceClassif.detectMultiScale(gray,1.3,5)
			for (x,y,w,h) in faces:
				rostro = auxFrame[y:y+h,x:x+w]
				rostro = cv2.resize(rostro,(150,150),interpolation= cv2.INTER_CUBIC)
				result = face_recognizer.predict(rostro)
				cv2.putText(frame,'{}'.format(result),(x,y-5),1,1.3,(255,255,0),1,cv2.LINE_AA)
				'''
				# EigenFaces
				if result[1] < 5700:
					cv2.putText(frame,'{}'.format(imagePaths[result[0]]),(x,y-25),2,1.1,(0,255,0),1,cv2.LINE_AA)
					cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
				else:
					cv2.putText(frame,'Desconocido',(x,y-20),2,0.8,(0,0,255),1,cv2.LINE_AA)
					cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)
				'''
				'''
				# FisherFace
				if result[1] < 500:
					cv2.putText(frame,'{}'.format(imagePaths[result[0]]),(x,y-25),2,1.1,(0,255,0),1,cv2.LINE_AA)
					cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
				else:
					cv2.putText(frame,'Desconocido',(x,y-20),2,0.8,(0,0,255),1,cv2.LINE_AA)
					cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)
				'''
				# LBPHFace
				if result[1] < 70:
					cv2.putText(frame,'{}'.format(imagePaths[result[0]]),(x,y-25),2,1.1,(0,255,0),1,cv2.LINE_AA)
					cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
					contador_p+=1
					if contador_p > UMBRAL_MATCHES_POSITIVOS:
						cap.release()
						cv2.destroyAllWindows()
						return True
				else:
					contador_n+=1
					if contador_n > UMBRAL_MATCHES_NEGATIVOS:
						cap.release()
						cv2.destroyAllWindows()
						return False
					cv2.putText(frame,'Desconocido',(x,y-20),2,0.8,(0,0,255),1,cv2.LINE_AA)
					cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)
				
			cv2.imshow('frame',frame)
			k = cv2.waitKey(1)
			if k == 27:
				break
		cap.release()
		cv2.destroyAllWindows()
		return False


if __name__=='__main__':

	face_recognition = ReconocimientoFacial()

	working_directory = face_recognition.prepare_working_directory("david")
	#face_recognition.get_samples_faces_from_cam(working_directory[1])
	#face_recognition.train_model(working_directory)
	face_recognition.reconocimiento_facial(working_directory)



