#!/usr/bin/python3

import serial
import time

class lecturatotal:
  def __init__(self,puerto, velocidad):
    self.puerto_serial = serial.Serial(puerto, velocidad)

  def leer_datos(self):
    return self.puerto_serial.readline().decode().strip()
  def imprimir_dato(self):
   print("El dato leido es: ")

arduino=lecturatotal('/dev/ttyACM0',9600)
temperaturas=[0]*10
while True:
	for i in range(10):
		temperaturas[i]=float(arduino.leer_datos())
		print(temperaturas[i])
		time.sleep(30)
	suma_vector=sum(temperaturas)
	promedio=suma_vector/10
	print("El promedio es ",promedio)

	with open("promedio_temperaturas.txt", "a") as archivo:
		archivo.write(str(promedio)+ "\n")





