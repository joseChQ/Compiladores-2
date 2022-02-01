from scanner.Analizador_Lexico import *
from scanner.Parser import *
from anytree import Node, RenderTree

archivo = ""
def imprimir_tokens(tokens):
	for token in tokens:
		temporal = ""
		if (token[0] == "ERROR"):
			temporal = archivo + ".txt: " + "LexicalError, line " + token[1] + "."
		else:
			temporal = "< " + token[0] + ", " + token[1] + " >" 	
		print (temporal)

def imprimir_errores(tokens):
	ok = False
	temporal = ""
	for token in tokens:
		temporal = ""
		linea = token[2]
		token_actual = token[1]
		if (token[0] == "ERROR"):
			temporal = archivo + ".txt: " + "LexicalError, line " + token[2] + "."
			codigo_error = ""
			pos_error = 0
			for token_error in tokens:
				if token_error[2] == linea:
					if token_error[1] == token_actual:
						pos_error = len(codigo_error) + len(token_actual) // 2 
					codigo_error += token_error[1] + ' '
			print(temporal)
			print("\t" + codigo_error)
			print("\t" + ' ' * pos_error + "^")
			ok = True
	return ok

def leer_archivo(nombre_archivo):
	super_string = ""
	lines = []
	with open("../files/" + nombre_archivo + ".txt") as f:
		lines = f.readlines()
	for line in lines:
		line_tmp = line
		line_tmp = line_tmp.strip()
		line_tmp += " @ "
		super_string += (line_tmp)
		#print(line)
	return super_string


def main():
	global archivo
	print("Enter the name of the file you want to read: ")
	archivo = input()	
	super_string = leer_archivo(archivo)


	# Analizador Lexico
	analizador = Analizador_Lexico()
	analizador.procesar(super_string)
	errores_lexicos = imprimir_errores(analizador.tokens)

	#for token in analizador.tokens:
	#	print("<",token[0],",",token[1],">")

	asignToken(analizador.tokens)
	if(Parse1()):
		printRoot1()
		print ("successful")
	current_token = get_token()
	#print("last_tokeen", current_token)

main()