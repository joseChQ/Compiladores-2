from anytree import Node, RenderTree

list_token = []
root = Node("Program")

def get_token():
	global list_token
	if len(list_token) == 0:
		return ["$","$"]
	tmp = list_token[0]
	return tmp

def u_token():
	global list_token
	list_token.pop(0)

def errores(a, line):
	print( "Se esperaba: ", a, " en la linea ",line)

def VarBlock(n_father): #VarBlock -> var VarList  |  3
	node = Node("VarBlock" , parent=n_father)

	current_token = get_token()
	if current_token[0] != "var":
		return False
	Node([current_token[0], current_token[1]] , parent=node)
	u_token()

	VarList(node)

	return True

def VarList(n_father): #VarList -> VarDecl : Type ; VarList|3
	node = Node("VarList" , parent=n_father)

	if not VarDecl(node):
		return False

	current_token = get_token()
	if current_token[0] != "PYP":
		return False
	Node([current_token[0], current_token[1]] , parent=node)
	u_token()

	if not Type(node):
		return False

	current_token = get_token()
	if current_token[0] != "PYCOM":
		return False
	Node(current_token , parent=node)
	u_token()

	VarList(node)
	return True

def Program(n_father): #Program -> program id; ConstBlock VarBlock MainCode
	node = Node("Program" , parent=n_father)

	current_token = get_token()
	if current_token[0] != "program":
		return False
	Node([current_token[0], current_token[1]], parent=node)
	u_token()

	current_token = get_token()
	if current_token[0] != "id":
		errores("id", current_token[2])
		return False
	Node([current_token[0], current_token[1]], parent=node)
	u_token()

	current_token = get_token()
	if current_token[0] != "PYCOM":
		errores(";", current_token[2])
		return False
	Node(current_token , parent=node)
	u_token()

	if not ConstBlock(node):
		return False

	if not VarBlock(node):
		return False

	if not MainCode(node):
		return False	

	return True

def MainCode(n_father):# MainCode -> begin StatementList end.
	node = Node("MainCode" , parent=n_father)

	current_token = get_token()
	if current_token[0] != "begin":
		return False
	Node([current_token[0], current_token[1]], parent=node)
	u_token()

	if not StatementList(node):
		return False

	current_token = get_token()
	if current_token[0] != "end":
		errores("end", current_token[2])
		return False
	Node([current_token[0], current_token[1]], parent=node)
	u_token()

	current_token = get_token()
	if current_token[0] != "DOT":
		errores(".", current_token[2])
		return False
	Node([current_token[0], current_token[1]], parent=node)
	u_token()

	return True

def ConstBlock(n_father):#ConstBlock -> const ConstList  |  3
	node = Node("ConstBlock" , parent=n_father)

	current_token = get_token()
	if current_token[0] != "const":
		return False
	Node([current_token[0], current_token[1]], parent=node)
	u_token()

	ConstList(node)

	return True

def ConstList(n_father):# ConstList -> id = Value; ConstList | 3
	node = Node("ConstList" , parent=n_father)

	current_token = get_token()
	if current_token[0] != "id":
		return False
	Node([current_token[0], current_token[1]], parent=node)
	u_token()

	current_token = get_token()
	if current_token[0] != "EQ":
		errores("=", current_token[2])
		return False
	Node([current_token[0], current_token[1]], parent=node)
	u_token()

	if not Value(node):
		return False

	current_token = get_token()
	if current_token[0] != "PYCOM":
		errores(";", current_token[2])
		return False
	Node([current_token[0], current_token[1]], parent=node)
	u_token()
	ConstList(node)
	return True

def VarDecl(n_father):#VarDecl → id | id, VarDecl
	node = Node("VarDecl" , parent=n_father)
	current_token = get_token()
	if current_token[0] != "id":
		return False
	Node([current_token[0], current_token[1]], parent=node)
	u_token()

	current_token = get_token()
	if current_token[0] == "COM":
		Node([current_token[0], current_token[1]], parent=node)
		u_token()
		return VarDecl(node)
	return True

def Type(n_father):#Type → real | integer | string
	node = Node("Type" , parent=n_father)
	current_token = get_token()
	if current_token[0] not in ["real","integer","string"]:
		return False
	node = Node([current_token[0], current_token[1]], parent=node)
	u_token()
	return True

def Value(n_father): # value -> numero|string
	node = Node("Value" , parent=n_father)
	current_token = get_token()
	if current_token[0] in ["numero","STR"]:
		Node([current_token[0], current_token[1]], parent=node)
		u_token()
	return True

def RelOp(n_father): # RelOp -> EQ | NQ | MENOR | MENOREQ | MAYOREQ | MAYOR
	current_token = get_token()
	node = Node("RelOp", parent=n_father)
	#print("RelOp ", current_token)
	if current_token[0] in ["EQ","NQ","MENOR","MENOREQ","MAYOREQ","MAYOR"]:
		Node([current_token[0], current_token[1]], parent=node)
		u_token()
		return True
	return False

def Factor(n_father): # Factor -> id | numero | ( Expr )
	current_token = get_token()
	node = Node("Factor", parent=n_father)
	#print("Factor ", current_token)
	if current_token[0] in ["id"]:
		Node([current_token[0], current_token[1]], parent=node)
		u_token()
		return True
	if Value(node):
		return True

	if current_token[0] =="A-P":
		Node(current_token[0] , parent=node)
		u_token()
		if not Expr(node):
			return False
		current_token = get_token()
		if current_token[0] != "C-P":
			return False
		Node(current_token[0] , parent=node)
		u_token()
		return True
	return False

def TermP(n_father): # Term' -> MULTI Factor Term' | DIV Factor Term' | MOD Factor Term' | 3
	current_token = get_token()
	node = Node("Term\'" , parent=n_father)
	#print("TermP", current_token)
	if current_token[0] in ["MULTI","DIVI","mod"]:
		Node([current_token[0], current_token[1]], parent=node)
		u_token()
		if not Factor(node):
			return False
		return TermP(node)
	if current_token[0] not in ['C-P', 'AND', 'EQ', 'MAYOR', 'MAYOREQ', 'MENOR', 'MENOREQ', 'NQ', 'OR', 'PYCOM', 'RESTA', 'SUMA', 'do']:
		return False
	return True
def Term(n_father): # Term -> Factor Term'
	current_token = get_token()
	node = Node("Term" , parent=n_father)
	#print("Term ", current_token)
	if not Factor(node):
		return False
	if not TermP(node):
		return False
	return True

def Expr3P(n_father): # Expr3' -> SUMA Term Expr3' | RESTA Term Expr3' | 3
	current_token = get_token()
	node = Node("Expr3\'" , parent=n_father)
	#print("Expr3P ", current_token)
	if current_token[0] in ["SUMA", "RESTA"]:
		Node([current_token[0], current_token[1]] , parent=node)
		u_token()
		if not Term(node):
			return False
		return Expr3P(node)
	if current_token[0] not in ['C-P', 'AND', 'EQ', 'MAYOR', 'MAYOREQ', 'MENOR', 'MENOREQ', 'NQ', 'OR', 'PYCOM', 'do']:
		return False
	return True;

def BooleanOp(n_father): # BooleanOp -> AND | OR
	current_token = get_token()
	node = Node("BooleanOp" , parent=n_father)
	#print("BooleanOp ", current_token)
	if current_token[0] in ["and","or"]:
		Node([current_token[0], current_token[1]] , parent=node)
		u_token()
		return True
	return False

def ExprP(n_father): # Expr' -> BooleanOp Expr2 Expr' | 3
	current_token = get_token()
	node = Node("Expr\'" , parent=n_father)
	if(BooleanOp(node)):
		if not Expr2(node):
			return False;
		return ExprP(node)
	#if(current_token[0] not in ['C-P', 'PYCOM', 'do']):
	#	return False
	return True

def Expr3(n_father): # Expr3 -> Term Expr3'
	current_token = get_token()
	node = Node("Expr3" , parent=n_father)
	if not Term(node):
		return False
	if not Expr3P(node):
		return False
	return True
def Expr2P(n_father): # Expr2' -> RelOp Expr3 Expr2' | 3 
	current_token = get_token()
	node = Node("Expr2\'" , parent=n_father)
	if RelOp(node):
		if not Expr3(node):
			return False
		return Expr2P(node)
	if current_token[0] not in ['C-P', 'AND', 'OR', 'PYCOM', 'do'] :
		return False
	return True

def Expr2(n_father): # Expr2 -> Expr3 Expr2'
	current_token = get_token()
	node = Node("Expr2" , parent=n_father)
	if not Expr3(node):
		return False
	if not Expr2P(node):
		return False
	return True

def Expr(n_father): # Expr -> Expr2 Expr'
	current_token = get_token()
	node = Node("Expr" , parent=n_father)
	if not Expr2(node):
		#if(current_token[2] == '23'):
			#print("ExprP2", current_token)
		return False
	if not ExprP(node):
		#if(current_token[2] == '23'):
			#print("ExprP", current_token)
		return False
	return True

def Assign(n_father): # Assign -> id ASIG Expr PYCOM
	node = Node("Assign" , parent=n_father)
	current_token = get_token()
	if current_token[0] != "id":
		return False
	Node([current_token[0], current_token[1]] , parent=node)
	u_token()
	current_token = get_token()
	if current_token[0] != "ASIG":
		return False
	Node([current_token[0], current_token[1]] , parent=node)
	u_token()
	if not Expr(node):
		return False
	current_token = get_token()
	if current_token[0] != "PYCOM":
		errores(";", current_token[2])
		return False
	Node([current_token[0], current_token[1]] , parent=node)
	u_token()
	return True


def Write(n_father): #Write -> write ( Expr )
	node = Node("Write" , parent=n_father)

	current_token = get_token()
	if current_token[0] != "write":
		return False
	u_token()

	current_token = get_token()
	if current_token[0] != "A-P":
		return False
	u_token()

	if not Expr():
		return False

	current_token = get_token()
	if current_token[0] != "C-P":
		return False
	u_token()

	return True

def WriteLn(n_father): #WriteLn -> writeln ( Expr );

	node = Node("WriteLn" , parent=n_father)

	current_token = get_token()
	if current_token[0] != "writeln":
		return False
	u_token()

	current_token = get_token()
	if current_token[0] != "A-P":
		errores("(", current_token[2])
		return False
	node = Node([current_token[0], current_token[1]], parent=node)
	u_token()

	if not Expr(node):
		return False

	current_token = get_token()
	if current_token[0] != "C-P":
		errores(")", current_token[2])
		return False
	node = Node([current_token[0], current_token[1]], parent=node)
	u_token()

	current_token = get_token()
	if current_token[0] != "PYCOM":
		errores(";", current_token[2])
		return False
	Node([current_token[0], current_token[1]], parent=node)
	u_token()

	return True
def Statement(n_father): #Statement -> Assign | ForStatement | IfStatement | Write | WriteLn | break | continue
	node = Node("Statement" , parent=n_father)
	current_token = get_token()
	node = Node("Statement" , parent=n_father)
	if (Assign(node) or ForStatement(node) or IfStatment(node) or Write(node) or WriteLn(node)):
		return True
	if current_token[0] in ["break","continue"]:
		Node([current_token[0], current_token[1]], parent=n_father)
		u_token()
		return True
	return False


	
def StatementList(n_father): #StatementList -> Statement StatementList'
	node = Node("StatementList" , parent=n_father)
	if Statement(node):
		if not StatementListP(node):
			return False
		return True
	return False

def StatementListP(n_father): #StatementList' -> 3 | StatementList
	node = Node("StatementList\'" , parent=n_father)
	current_token = get_token()
	if (current_token[0] in ['break', 'continue', 'for', 'id', 'if', 'write', 'writeln']):
		return StatementList(node)
	if(current_token[0] in ['end']):
		return True
	return False

def IfStatment(n_father): #IfStatement -> if ( Expr ) then begin StatementList end ; else begin StatementList end ;	
	node = Node("IfStatement" , parent=n_father)

	current_token = get_token()
	if current_token[0] != "if":
		return False
	Node([current_token[0], current_token[1]], parent=node)
	
	u_token()

	current_token = get_token()
	if current_token[0] != "A-P":
		errores("(", current_token[2])
		return False
	Node([current_token[0], current_token[1]], parent=node)
	
	u_token()

	current_token = get_token()
	#print("antes de jose3 ", current_token)
	if not Expr(node):
	#	print("josecin", current_token)
		return False

	current_token = get_token()
	if current_token[0] != "C-P":
		errores(")", current_token[2])
		return False
	Node([current_token[0], current_token[1]], parent=node)
	u_token()

	current_token = get_token()
	if current_token[0] != "then":
		errores("then", current_token[2])
		return False
	Node([current_token[0], current_token[1]], parent=node)
	u_token()

	current_token = get_token()
	if current_token[0] != "begin":
		errores("begin", current_token[2])
		return False
	Node([current_token[0], current_token[1]], parent=node)
	u_token()

	if not StatementList(node):
		return False

	current_token = get_token()
	if current_token[0] != "end":
		errores("end", current_token[2])
		return False
	Node([current_token[0], current_token[1]], parent=node)
	u_token()

	current_token = get_token()
	if current_token[0] != "PYCOM":
		errores(";", current_token[2])
		return False
	Node([current_token[0], current_token[1]], parent=node)
	u_token()

	current_token = get_token()
	if current_token[0] != "else":
		errores("else", current_token[2])
		return False
	Node([current_token[0], current_token[1]], parent=node)
	u_token()

	current_token = get_token()
	if current_token[0] != "begin":
		errores("begin", current_token[2])
		return False
	Node([current_token[0], current_token[1]], parent=node)
	u_token()

	if not StatementList(node):
		return False

	current_token = get_token()
	if current_token[0] != "end":
		errores("end", current_token[2])
		return False
	Node([current_token[0], current_token[1]], parent=node)
	u_token()

	current_token = get_token()
	if current_token[0] != "PYCOM":
		errores(";", current_token[2])
		return False
	Node([current_token[0], current_token[1]], parent=node)
	u_token()

	return True


def ForStatement(n_father):# ForStatement -> for id := Value to Expr do begin StatementList end ;
	node = Node("ForStatement" , parent=n_father)
	current_token = get_token()
	if current_token[0] != "for":
		return False
	Node([current_token[0], current_token[1]], parent=node)
	u_token()

	current_token = get_token()
	if current_token[0] != "id":
		errores("id", current_token[2])
		return False
	Node([current_token[0], current_token[1]], parent=node)
	u_token()

	current_token = get_token()
	if current_token[0] != "ASIG":
		errores(":=", current_token[2])
		return False
	Node([current_token[0], current_token[1]], parent=node)
	u_token()

	if not Value(node):
		return False

	current_token = get_token()
	if current_token[0] != "to":
		errores("to", current_token[2])
		return False
	Node([current_token[0], current_token[1]], parent=node)
	u_token()

	if not Expr(node):
		return False

	current_token = get_token()
	if current_token[0] != "do":
		errores("do", current_token[2])
		return False
	Node([current_token[0], current_token[1]], parent=node)
	u_token()

	current_token = get_token()
	if current_token[0] != "begin":
		errores("begin", current_token[2])
		return False	
	Node([current_token[0], current_token[1]], parent=node)
	u_token()

	if not StatementList(node):
		return False

	current_token = get_token()
	if current_token[0] != "end":
		errores("end", current_token[2])
		return False
	Node([current_token[0], current_token[1]], parent=node)	
	u_token()

	current_token = get_token()
	if current_token[0] != "PYCOM":
		errores(";", current_token[2])
		return False	
	Node([current_token[0], current_token[1]], parent=node)
	u_token()

	return True

def Parse1():
	global root
	return Program(root)

def asignToken(Original_Tokens):
	global list_token
	#for token in Original_Tokens:
		#list_token.append([token[0],token[1]])
	list_token = Original_Tokens
	#for token in list_token:
	#	print(token[0],token[1])


def printRoot1():
	global root
	for pre, fill, node in RenderTree(root):
		print(f"{pre}{node.name}")
