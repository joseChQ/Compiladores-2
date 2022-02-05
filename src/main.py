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
			temporal2 = ''
			for c in codigo_error:
				if c =='@':
					temporal2+=' '
				else:
					temporal2+=c
			print(temporal)
			print("\t" + temporal2)
			print("\t" + ' ' * pos_error + "^")
			ok = True
	return ok

def tokensWithOutErrors(tokens):
	ok = False
	tmp = []
	for token in tokens:
		
		if (token[0] != "ERROR"):
			tmp.append(token)				

	return tmp

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
	tokens_with_out_error = tokensWithOutErrors(analizador.tokens)
	#for token in analizador.tokens:
	#	print("<",token[0],",",token[1],">")

	asignToken(tokens_with_out_error)
	#print(tokens_with_out_error)
	if(Parse1()):
		#printRoot1()
		print ("successful")
	else:
		printError()
	#print(tokens_with_out_error)
	#printRoot1()
	current_token = get_token()
	#print("last_tokeen", current_token)

main()