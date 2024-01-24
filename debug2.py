import sys

#Datos Prueba:
usuario = "ezeleo"
puntos = 200
level = 5
time = "45:45:4"

encontro = False

#Agregado de elemento (Desordenado)
archivo = open("stats.txt",'r+')

linea = archivo.readline()
while (linea != ""):
	linea = archivo.readline()
	cad = linea.replace('\n','')
	cad = cad.split(';')

	#Busca en la lista si no hay datos que no coincidan
	if (linea != "")and(cad[0]==usuario)and(cad[1]==str(puntos))and(cad[2]==str(level)and(cad[3]==str(time))):
		encontro = True

	#Guarda en la ultima linea vacia si no existe el dato 
	if (linea == "")and(encontro==False):
		archivo.write("\n"+usuario+";"+str(puntos)+";"+str(level)+";"+str(time))
		

if (linea == ""):
	print(True)
else:
	print(False)				

archivo.close()




#Lectura de archivo y ordenado

archivo = open("stats.txt",'r')

vector = []

linea = archivo.readline()
while(linea!=""):
	linea = archivo.readline()
	cad = linea.replace('\n','')
	if cad != "":
		vector.append([])
		vector[len(vector)-1] = cad.split(';')

archivo.close()


#Ordenado de vector
for i in range(len(vector)):
	for j in range(len(vector)-1):
		if (int(vector[j][1]) < int(vector[j+1][1])):
			temp = vector[j]
			vector[j] = vector[j+1]
			vector[j+1] = temp


for i in range(0,len(vector)):
	print(vector[i])

