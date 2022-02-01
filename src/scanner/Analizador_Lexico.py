palabras_reservadas = ["array", "begin", "case", "const", "do", "downto", "else",
	"end", "file", "for", "function", "goto", "if", "label", "nil", "of", "packed",
	"procedure", "program", "record", "repeat", "set", "then", "to", "type", "until",
	"var", "while", "with", "and","or", "not", "div", "mod", "in", "write", "writeln", "real", "integer", "string"]

operadores = ["+", "-", "*", "/", ":=", "=", "<>", "<", "<=", ">=", ">" ,"^"]
op_etiquetas = ["SUMA", "RESTA", "MULTI", "DIVI","ASIG", "EQ", "NQ", "MENOR", "MENOREQ", "MAYOREQ", "MAYOR", "XOR"]
delimitadores = [",", ";", ":", "(", ")", "[", "]", ".", ".."]
deli_etiquetas = ["COM", "PYCOM", "PYP", "A-P", "C-P", "A-C", "C-C", "DOT", "TWODOT"]

def encontrar_operador(c):
	for operador in operadores:
		if (operador[0] == c):
			return True
	return False

def encontrar_delimitador(c):
	for delimitador in delimitadores:
		if (delimitador[0] == c):
			return True
	return False
def es_punto_decimal(a, b, c):
	if ((a >= '0' and a <= '9') and (c >= '0' and c <= '9' or c == 'e') and b == '.'):
		return True
	return False
def guardar_tokens():
	archivo = open("Salida_tokens.txt", "a")
	for token in tokens:
		archivo.write(token + '\n')
	archivo.close()
def transformar_numero(palabra):
	numero_expo = palabra.split('e')
	numero_final = float(numero_expo[0])
	#print("tt", numero_final, numero_expo)
	if(len(numero_expo) == 2):
		expo = int(numero_expo[1][1:])
		if(numero_expo[1][0] =='+'):
			for i in range(expo):
				numero_final *= 10
		else:
			for i in range(expo):
				numero_final /= 10
	return str(numero_final)


class Analizador_Lexico:
	diccionario = dict() # <+, SUMA>
	tokens = []
	def __init__ (self):
		# Incluyendo palabras reservadas
		for palabra in palabras_reservadas:
			self.diccionario[palabra] = palabra

		# Incluyendo operadores
		for i in range(len(operadores)):
			self.diccionario[operadores[i]] = op_etiquetas[i]

		# Incluyendo delimitadores
		for i in range(len(delimitadores)):
			self.diccionario[delimitadores[i]] = deli_etiquetas[i]
	def es_numero (self, palabra):

		# dividir la palabra por e

		numero = palabra.split('e')
		#print("numero:",numero)
		if(palabra[0] == 'e' or palabra[0] == '.' or palabra[-1] == '.'or numero[0][-1] == '.' or numero[0].count('.')>1):
			return False

		for i in range(len(numero[0])):
			if(numero[0][i] != '.' and (numero[0][i] < '0' or numero[0][i] > '9')):
				return False
		#print("palabra: ", numero, numero[0][0])
		if len(numero) >= 2:
			if len(numero[1]) <= 1 and ('e' not in palabra):
				return False
			if len(numero[1]):
				if(numero[1][0] != '-' and numero[1][0] != '+'):
					return False
				for i in range(1,len(numero[1])):
					if(numero[1][i] < '0' or numero[1][i] > '9'):
						return False
		return True

	def es_identificador (self, palabra):
		i = 0
		if (not((palabra[i] >= 'a' and palabra[i] <= 'z') or (palabra[i] >= 'A' and palabra[i] <= 'Z'))):
			return False
			
		i +=1
		for j in range(i, len(palabra)):
			if (not((palabra[j] >= 'a' and palabra[j] <= 'z') or (palabra[j] >= 'A' and palabra[j] <= 'Z') or (palabra[j] >= '0' and palabra[j] <= '9'))):
				return False
		return True
	
	def es_string (self, palabra):
		return (palabra[0] == '\'' and palabra[len(palabra) - 1] == '\'')	

	def generar_token (self, palabra, numero_de_linea):
		# Palabras reservadas, identificadores ya leidos, delimitadores y operadores
		if (palabra in self.diccionario):
			return [self.diccionario[palabra], palabra , str(numero_de_linea)]
		
		# Numeros
		if (self.es_numero(palabra)):
			return ["numero", transformar_numero(palabra), str(numero_de_linea)]

		# Identificador nuevo
		if (self.es_identificador(palabra)):
			self.diccionario[palabra] = "id"
			return ["id", palabra, str(numero_de_linea)]
		
		# String
		if (self.es_string(palabra)):
			palabra_nueva = ""
			for i  in range(1,len(palabra)-1):
				if(  i + 1 < len(palabra) and palabra[i] == '\'' and palabra[i + 1] == '\'' ):
					continue
				palabra_nueva += palabra[i]

			return ["STR", palabra_nueva, str(numero_de_linea)]

		return ["ERROR", palabra, str(numero_de_linea)]


	def procesar(self, super_string):
		i = 0
		j = 1
		n = len(super_string)
		numero_de_linea_actual = 1
		#print(super_string)
		while (i < n):
			if (super_string[i] == '@'):
				numero_de_linea_actual += 1
				i += 1
				j = i + 1			
			elif (super_string[i] == ' ' or super_string[i] == '\t'):
				i += 1
				j = i + 1				
			else:
				#print("entro delimitadores", super_string[i], super_string[i+1])
				if (super_string[i] == '{'): # Comentario
					if (j == n or super_string[j] == '}'):
						i = min(j + 1, n)
						j = i
				elif (i + 1 < n and super_string[i] == '(' and super_string[i + 1] == '*' ): # comentario (* ... *)
					if(j == n or (j + 1 < n and super_string[j] == '*' and super_string[j+1] == ')')):
						i = min(j + 2, n)
						j = i
				elif (j + 1 < n and es_punto_decimal(super_string[j-1],super_string[j],super_string[j+1])): #54.54
					j += 1
					#print("entro 2")

				elif (i + 1 < n and super_string[i] == '.' and super_string[i + 1] == '.'): # caso especial ..
					tmp = super_string[i : i + 2]
					self.tokens.append(self.generar_token(tmp, numero_de_linea_actual))
					i += 2
					j = i
					#print("entro")
				elif (super_string[i] == '\''): # String
					if (j +1 < n and super_string[j] == '\'' and super_string[j + 1] == '\''):
						j += 1
					elif (j == n or super_string[j] == '\''):
						tmp = super_string[i : min(j + 1, n )] # 'cdcdcdcd'sdf
						self.tokens.append((self.generar_token(tmp, numero_de_linea_actual)))
						i = min(j + 1, n)
						j = i	
				elif (i + 1 < n and encontrar_delimitador(super_string[i]) and super_string[i+1] != '='):
					tmp = super_string[i : i + 1]
					self.tokens.append(self.generar_token(tmp, numero_de_linea_actual))
					i += 1
					j = i		
									
				elif (encontrar_operador(super_string[i])):
					if (i + 1 < n and (super_string[i + 1] == '=' or super_string[i + 1] == '>' )): # Operador de 2 caracteres
						tmp = super_string[i : i + 2]
						self.tokens.append(self.generar_token(tmp, numero_de_linea_actual))
						i += 2
						j = i
					else: # Operador de 1 caracter
						tmp = super_string[i : i + 1]
						self.tokens.append(self.generar_token(tmp, numero_de_linea_actual))
						i += 1
						j = i									
				elif (j == n or super_string[j] == ' ' or super_string[j] == '\t' or (encontrar_operador(super_string[j]) and  super_string[j-1] != 'e') or encontrar_delimitador(super_string[j])):
					tmp = super_string[i : j]
					self.tokens.append(self.generar_token(tmp , numero_de_linea_actual))
					i = j
				j += 1
