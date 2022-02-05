from anytree import Node, RenderTree

list_token = []
root = Node("Program")
list_errores = []

linea = 0
def get_token():
	global list_token
	global linea
	if len(list_token) == 0:
		return ['$','$',linea]
	tmp = list_token[0]

	linea = tmp[2]

	return tmp

def u_token():
	global list_token
	if len(list_token):
		list_token.pop(0)

def errores():
	current_token = get_token()
	tmp = "no esperado: " + current_token[1] + " en la linea " + current_token[2]
	list_errores.append(tmp)

def VarBlock(n_father): #VarBlock -> var VarList  |  3
	node = Node("VarBlock" , parent=n_father)

	current_token = get_token()
	if current_token[0] == "var":
		Node([current_token[0], current_token[1]] , parent=node)
		u_token()

		VarList(node)
		return None

	#if(current_token[0] != 'begin'): #FOLLOW(VarBlock) = ['$', 'begin']
	#while (current_token[0] is not  ['begin','$']):
	#	u_token()
	#	current_token = get_token()
	return None

def VarList(n_father): #VarList -> VarDecl : Type ; VarList|3
	node = Node("VarList" , parent=n_father)
	#VarList
	current_token = get_token()
	if (current_token[0] == 'id'):#FIRST(VarDecl) = ['id']
		VarDecl(node)
		current_token = get_token()
		if current_token[0] != "PYP": # FOLLOW(VarList) = ['$', 'begin']
			errores()
			while current_token[0] not in ['begin', '$']:
				u_token()
				current_token = get_token()
			return None

		Node([current_token[0], current_token[1]] , parent=node)
		u_token()

		Type(node)

		current_token = get_token()
		if current_token[0] != "PYCOM": # FOLLOW(VarList) = ['$', 'begin']
			errores()
			while current_token[0] not in ['begin', '$']:
				u_token()
				current_token = get_token()
			return None
		Node(current_token , parent=node)
		u_token()

		return VarList(node)	
	return None

def Program(n_father): #Program -> program id; ConstBlock VarBlock MainCode
	node = Node("Program" , parent=n_father)

	current_token = get_token()
	if current_token[0] != "program":
		return False
	Node([current_token[0], current_token[1]], parent=node)
	u_token()

	current_token = get_token()
	if current_token[0] != "id":
		errores()
		while current_token[0] not in ["$"]:
			u_token()
			current_token = get_token()
		return None
	Node([current_token[0], current_token[1]], parent=node)
	u_token()

	current_token = get_token()
	if current_token[0] != "PYCOM":
		errores()
		while current_token[0] not in ["$"]:
			u_token()
			current_token = get_token()
		return None
	Node(current_token , parent=node)
	u_token()

	ConstBlock(node)
	#print("ConstBlock")
	VarBlock(node)
	#print("VarBlock")
	MainCode(node)
	#print("MainCode")
	return None

def MainCode(n_father):# MainCode -> begin StatementList end.
	node = Node("MainCode" , parent=n_father)

	current_token = get_token()
	if current_token[0] != "begin":
		return False
	Node([current_token[0], current_token[1]], parent=node)
	u_token()

	StatementList(node)


	current_token = get_token()
	if current_token[0] != "end":
		errores()
		while current_token[0] not in ['$']:
			u_token()
			current_token = get_token()
		return None
	Node([current_token[0], current_token[1]], parent=node)
	u_token()


	current_token = get_token()

	if current_token[0] != "DOT":
		errores()
		while current_token[0] not in ['$']:
			u_token()
			current_token = get_token()
		return None
	Node([current_token[0], current_token[1]], parent=node)
	u_token()

	return None
###################################################################
def ConstBlock(n_father):#ConstBlock -> const ConstList  |  3
	node = Node("ConstBlock" , parent=n_father)

	current_token = get_token()
	if current_token[0] == "const":
		Node([current_token[0], current_token[1]], parent=node)
		u_token()
		ConstList(node)
		return None
	

def ConstList(n_father):# ConstList -> id := Value; ConstList | 3
	node = Node("ConstList" , parent=n_father)

	current_token = get_token()
	if current_token[0] != "id":
		return False
	Node([current_token[0], current_token[1]], parent=node)
	u_token()

	current_token = get_token()
	if current_token[0] != "ASIG":
		errores()
		#FOLLOW(ConstList) = ['begin', 'var','$']
		while current_token[0] not in ['begin', 'var','$']:
			u_token()
			current_token = get_token()
		return None
	Node([current_token[0], current_token[1]], parent=node)
	u_token()

	current_token = get_token()
	if current_token [0] not in ['STR','numero']:
		errores()
		#FOLLOW(ConstList) = ['begin', 'var','$']
		while current_token[0] not in ['begin', 'var','$']:
			u_token()
			current_token = get_token()
		return None
	Value(node)

	current_token = get_token()
	if current_token[0] != "PYCOM":
		#FOLLOW(ConstList) = ['begin', 'var','$']
		while current_token[0] not in ['begin', 'var','$']:
			u_token()
			current_token = get_token()
		return None

	Node([current_token[0], current_token[1]], parent=node)
	u_token()
	ConstList(node)
	return None

def VarDecl(n_father):#VarDecl → id | id, VarDecl
	node = Node("VarDecl" , parent=n_father)
	current_token = get_token()
	if current_token[0] != "id":
		return None
	Node([current_token[0], current_token[1]], parent=node)
	u_token()

	current_token = get_token()
	if current_token[0] == "COM":
		Node([current_token[0], current_token[1]], parent=node)
		u_token()
		return VarDecl(node)
	return None

def Type(n_father):#Type → real | integer | string
	node = Node("Type" , parent=n_father)
	current_token = get_token()
	if current_token[0] not in ["real","integer","string"]:
		return None
	node = Node([current_token[0], current_token[1]], parent=node)
	u_token()
	return None

def Value(n_father): # value -> numero|string
	node = Node("Value" , parent=n_father)
	current_token = get_token()
	if current_token[0] in ["numero","STR"]:
		Node([current_token[0], current_token[1]], parent=node)
		u_token()
	return None

def RelOp(n_father): # RelOp -> EQ | NQ | MENOR | MENOREQ | MAYOREQ | MAYOR
	current_token = get_token()
	#print("RelOp ", current_token)
	if current_token[0] in ["EQ","NQ","MENOR","MENOREQ","MAYOREQ","MAYOR"]:
		node = Node("RelOp", parent=n_father)
		Node([current_token[0], current_token[1]], parent=node)
		u_token()
		return None
	return None

def Factor(n_father): # Factor -> id | value | ( Expr )
	current_token = get_token()
	node = Node("Factor", parent=n_father)
	#print("Factor ", current_token)
	if current_token[0] in ["id"]:
		Node([current_token[0], current_token[1]], parent=node)
		u_token()
		return None

	current_token = get_token()
	if current_token[0] in ["numero","STR"]:
		Value(node)
		return None
	

	if current_token[0] =="A-P":
		Node(current_token[0] , parent=node)
		u_token()
		Expr(node)
		current_token = get_token()
		if current_token[0] != "C-P":
			#FOLLOW(Factor) = [')', 'AND', 'DIVI', 'EQ', 'MAYOR', 'MAYOREQ', 'MENOR', 'MENOREQ', 'MOD', 'MULTI', 'NQ', 'OR', 'PYCOM', 'RESTA', 'SUMA', 'do']
			errores()
			while current_token[0] not in ['C-P', 'and', 'DIVI', 'EQ', 'MAYOR', 'MAYOREQ', 'MENOR', 'MENOREQ', 'MOD', 'MULTI', 'NQ', 'OR', 'PYCOM', 'RESTA', 'SUMA', 'do','$']:
				u_token()
				current_token = get_token()
			return None
		Node(current_token[0] , parent=node)
		u_token()
		return None
	return None

def TermP(n_father): # Term' -> MULTI Factor Term' | DIV Factor Term' | MOD Factor Term' | 3
	current_token = get_token()
	#print("TermP ",current_token)
	node = Node("Term\'" , parent=n_father)
	#print("TermP", current_token)
	if current_token[0] in ["MULTI","DIVI","mod"]:
		Node([current_token[0], current_token[1]], parent=node)
		u_token()
		Factor(node)
		return TermP(node)
#	while current_token[0] not in ['C-P', 'AND', 'EQ', 'MAYOR', 'MAYOREQ', 'MENOR', 'MENOREQ', 'NQ', 'OR', 'PYCOM', 'RESTA', 'SUMA', 'do','$']:
#		u_token()
#		current_token = get_token()
	return None

def Term(n_father): # Term -> Factor Term'
	current_token = get_token()
	#print("Term ",current_token)
	node = Node("Term" , parent=n_father)
	#print("Term ", current_token)
	Factor(node)
	TermP(node)
	return None

def Expr3P(n_father): # Expr3' -> SUMA Term Expr3' | RESTA Term Expr3' | 3
	current_token = get_token()
	#print("Expr3P ",current_token)
	node = Node("Expr3\'" , parent=n_father)
	#print("Expr3P ", current_token)
	if current_token[0] in ["SUMA", "RESTA"]:
		Node([current_token[0], current_token[1]] , parent=node)
		u_token()
		Term(node)
		Expr3P(node)
		return None
	#while current_token[0] not in ['C-P', 'AND', 'EQ', 'MAYOR', 'MAYOREQ', 'MENOR', 'MENOREQ', 'NQ', 'OR', 'PYCOM', 'do','$']:
	#	u_token()
	#	current_token = get_token()
	return None;

def BooleanOp(n_father): # BooleanOp -> AND | OR
	current_token = get_token()
	node = Node("BooleanOp" , parent=n_father)
	#print("BooleanOp ", current_token)
	if current_token[0] in ["and","or"]:
		Node([current_token[0], current_token[1]] , parent=node)
		u_token()
		return None
	return None

def ExprP(n_father): # Expr' -> BooleanOp Expr2 Expr' | 3
	current_token = get_token()
	#print("ExprP ",current_token)
	#FIRST(BooleanOp) = ['AND', 'OR']
	if current_token[0] in ["and","or"]:
		node = Node("Expr\'" , parent=n_father)
		BooleanOp(node)
		Expr2(node)
		ExprP(node)
		return None
	current_token = get_token()
	#FOLLOW(Expr') = [')', 'PYCOM', 'do']
	#if(current_token[0] not in ['C-P', 'PYCOM', 'do']):
	#while current_token[0] not  in ['C-P', 'PYCOM', 'do', '$']:
	#	u_token()
	#	current_token = get_token()
	#	return False
	return None

def Expr3(n_father): # Expr3 -> Term Expr3'
	current_token = get_token()
	#print("Expr3", current_token)
	node = Node("Expr3" , parent=n_father)
	Term(node)
	Expr3P(node)
	return None

def Expr2P(n_father): # Expr2' -> RelOp Expr3 Expr2' | 3 
	current_token = get_token()
	#print("Expr2P",current_token)
	node = Node("Expr2\'" , parent=n_father)
	#FIRST(RelOp) = ['EQ', 'MAYOR', 'MAYOREQ', 'MENOR', 'MENOREQ', 'NQ']
	if current_token[0] in['EQ', 'MAYOR', 'MAYOREQ', 'MENOR', 'MENOREQ', 'NQ']:
		RelOp(node)
		Expr3(node)
		return Expr2P(node)

	#FOLLOW(Expr2') = [')', 'AND', 'OR', 'PYCOM', 'do']
	current_token = get_token()
	#while current_token[0] not in ['C-P', 'AND', 'OR', 'PYCOM', 'do','$'] :
	#	u_token()
	#	current_token = get_token()
	return None

def Expr2(n_father): # Expr2 -> Expr3 Expr2'
	current_token = get_token()
	#print("Expr2", current_token)
	node = Node("Expr2" , parent=n_father)
	Expr3(node)
	Expr2P(node)
	return None

def Expr(n_father): # Expr -> Expr2 Expr'
	current_token = get_token()
	#print("Expr",current_token)
	node = Node("Expr" , parent=n_father)
	Expr2(node)
	ExprP(node)
	return None

def Assign(n_father): # Assign -> id ASIG Expr PYCOM
	node = Node("Assign" , parent=n_father)
	current_token = get_token()
	if current_token[0] != "id":
		return None
	Node([current_token[0], current_token[1]] , parent=node)
	u_token()
	current_token = get_token()
	if current_token[0] != "ASIG":
		#FOLLOW(Assign) = ['break', 'continue', 'end', 'for', 'id', 'if', 'write', 'writeln','$']
		errores()
		while current_token[0] not in ['break', 'continue', 'end', 'for', 'id', 'if', 'write', 'writeln','$']:
			u_token()
			current_token = get_token()
		return None 
	Node([current_token[0], current_token[1]] , parent=node)
	u_token()
	#print("current_token mucho antes: ",current_token)
	Expr(node)
	current_token = get_token()
	#print("current_token antes: ",current_token)
	if current_token[0] != "PYCOM":
		#FOLLOW(Assign) = ['break', 'continue', 'end', 'for', 'id', 'if', 'write', 'writeln','$']
		errores()
		while current_token[0] not in ['break', 'continue', 'end', 'for', 'id', 'if', 'write', 'writeln','$']:
			u_token()
			current_token = get_token()
		#print("current_token: ",current_token)
		return None
	Node([current_token[0], current_token[1]] , parent=node)
	u_token()
	return None


def Write(n_father): #Write -> write ( Expr )
	node = Node("Write" , parent=n_father)

	current_token = get_token()
	if current_token[0] != "write":
		return None
	u_token()

	current_token = get_token()
	if current_token[0] != "A-P":
		errores()
		#FOLLOW(Write) = ['break', 'continue', 'end', 'for', 'id', 'if', 'write', 'writeln']
		while current_token[0] not in  ['break', 'continue', 'end', 'for', 'id', 'if', 'write', 'writeln', '$']:
			u_token()
			current_token = get_token()
		return None
	u_token()

	Expr(node)
	current_token = get_token()
	if current_token[0] != "C-P":
		errores()
		#FOLLOW(Write) = ['break', 'continue', 'end', 'for', 'id', 'if', 'write', 'writeln']
		while current_token[0] not in  ['break', 'continue', 'end', 'for', 'id', 'if', 'write', 'writeln', '$']:
			u_token()
			current_token = get_token()
		return None
	u_token()

	return None

def WriteLn(n_father): #WriteLn -> writeln ( Expr );

	node = Node("WriteLn" , parent=n_father)

	current_token = get_token()
	if current_token[0] != "writeln":
		return None
	u_token()
	current_token = get_token()
	if current_token[0] != "A-P":
		errores()
		#FOLLOW(WriteLn) = ['break', 'continue', 'end', 'for', 'id', 'if', 'write', 'writeln']
		while current_token[0] not in ['break', 'continue', 'end', 'for', 'id', 'if', 'write', 'writeln', '$']:
			u_token()
			current_token = get_token()
		return None

	node = Node([current_token[0], current_token[1]], parent=node)
	u_token()
	Expr(node)
	current_token = get_token()
	if current_token[0] != "C-P":
		errores()
		#FOLLOW(WriteLn) = ['break', 'continue', 'end', 'for', 'id', 'if', 'write', 'writeln']
		while current_token[0] not in ['break', 'continue', 'end', 'for', 'id', 'if', 'write', 'writeln', '$']:
			u_token()
			current_token = get_token()
		return None
	node = Node([current_token[0], current_token[1]], parent=node)
	u_token()
	current_token = get_token()
	if current_token[0] != "PYCOM":
		errores()
		#FOLLOW(WriteLn) = ['break', 'continue', 'end', 'for', 'id', 'if', 'write', 'writeln']
		while current_token[0] not in ['break', 'continue', 'end', 'for', 'id', 'if', 'write', 'writeln', '$']:
			u_token()
			current_token = get_token()
		return None
	Node([current_token[0], current_token[1]], parent=node)
	u_token()
	return None


def Statement(n_father): #Statement -> Assign | ForStatement | IfStatement | Write | WriteLn | break | continue
	node = Node("Statement" , parent=n_father)
	Assign(node)
	ForStatement(node)
	IfStatment(node)
	Write(node)
	WriteLn(node)
	current_token = get_token()

	if current_token[0] in ["break","continue"]:
		Node([current_token[0], current_token[1]], parent=n_father)
		u_token()
		return None
	return None
	
def StatementList(n_father): #StatementList -> Statement StatementList'
	#FIRST(Statement) = ['break', 'continue', 'for', 'id', 'if', 'write', 'writeln']
	#current_token = get_token()
	node = Node("StatementList" , parent=n_father)
	Statement(node)
	StatementListP(node)
	
	return None

def StatementListP(n_father): #StatementList' -> 3 | StatementList
	node = Node("StatementList\'" , parent=n_father)

	current_token = get_token()
	#FIRST(StatementList) = ['break', 'continue', 'for', 'id', 'if', 'write', 'writeln']
	if (current_token[0] in ['break', 'continue', 'for', 'id', 'if', 'write', 'writeln']):
		return StatementList(node)

	current_token = get_token()
	#FOLLOW(StatementList') = ['end', '$']
	while current_token[0] not in ['end','$']:
		u_token()
		current_token = get_token()
	return None

def IfStatment(n_father): #IfStatement -> if ( Expr ) then begin StatementList end ; else begin StatementList end ;	
	node = Node("IfStatement" , parent=n_father)

	current_token = get_token()
	if current_token[0] != "if":
		return None
	Node([current_token[0], current_token[1]], parent=node)
	
	u_token()

	current_token = get_token()
	if current_token[0] != "A-P":
		errores()
		#FOLLOW(IfStatement) = ['break', 'continue', 'end', 'end.', 'for', 'id', 'if', 'write', 'writeln', '$']
		while current_token[0] not in ['break', 'continue', 'end', 'end.', 'for', 'id', 'if', 'write', 'writeln', '$']:
			u_token()
			current_token = get_token()
		return None
	Node([current_token[0], current_token[1]], parent=node)
	
	u_token()

	current_token = get_token()

	Expr(node)
	current_token = get_token()
	if current_token[0] != "C-P":
		errores()
		#FOLLOW(IfStatement) = ['break', 'continue', 'end', 'end.', 'for', 'id', 'if', 'write', 'writeln', '$']
		while current_token[0] not in ['break', 'continue', 'end', 'end.', 'for', 'id', 'if', 'write', 'writeln', '$']:
			u_token()
			current_token = get_token()
		return None
	Node([current_token[0], current_token[1]], parent=node)
	u_token()

	current_token = get_token()
	if current_token[0] != "then":
		errores()
		#FOLLOW(IfStatement) = ['break', 'continue', 'end', 'end.', 'for', 'id', 'if', 'write', 'writeln', '$']
		while current_token[0] not in ['break', 'continue', 'end', 'end.', 'for', 'id', 'if', 'write', 'writeln', '$']:
			u_token()
			current_token = get_token()
		#return None
	Node([current_token[0], current_token[1]], parent=node)
	u_token()

	current_token = get_token()
	if current_token[0] != "begin":
		errores()
		#FOLLOW(IfStatement) = ['break', 'continue', 'end', 'end.', 'for', 'id', 'if', 'write', 'writeln', '$']
		while current_token[0] not in ['break', 'continue', 'end', 'end.', 'for', 'id', 'if', 'write', 'writeln', '$']:
			u_token()
			current_token = get_token()
		#return None
	Node([current_token[0], current_token[1]], parent=node)
	u_token()

	StatementList(node)


	current_token = get_token()
	if current_token[0] != "end":
		errores()
		#FOLLOW(IfStatement) = ['break', 'continue', 'end', 'end.', 'for', 'id', 'if', 'write', 'writeln', '$']
		while current_token[0] not in ['break', 'continue', 'end', 'end.', 'for', 'id', 'if', 'write', 'writeln', '$']:
			u_token()
			current_token = get_token()
		return None
	Node([current_token[0], current_token[1]], parent=node)
	u_token()

	current_token = get_token()
	if current_token[0] != "PYCOM":
		errores()
		#FOLLOW(IfStatement) = ['break', 'continue', 'end', 'end.', 'for', 'id', 'if', 'write', 'writeln', '$']
		while current_token[0] not in ['break', 'continue', 'end', 'end.', 'for', 'id', 'if', 'write', 'writeln', '$']:
			u_token()
			current_token = get_token()
		return None
	Node([current_token[0], current_token[1]], parent=node)
	u_token()

	current_token = get_token()
	if current_token[0] != "else":
		errores()
		#FOLLOW(IfStatement) = ['break', 'continue', 'end', 'end.', 'for', 'id', 'if', 'write', 'writeln', '$']
		while current_token[0] not in ['break', 'continue', 'end', 'end.', 'for', 'id', 'if', 'write', 'writeln', '$']:
			u_token()
			current_token = get_token()
		return None
	Node([current_token[0], current_token[1]], parent=node)
	u_token()

	current_token = get_token()
	if current_token[0] != "begin":
		errores()
		#FOLLOW(IfStatement) = ['break', 'continue', 'end', 'end.', 'for', 'id', 'if', 'write', 'writeln', '$']
		while current_token[0] not in ['break', 'continue', 'end', 'end.', 'for', 'id', 'if', 'write', 'writeln', '$']:
			u_token()
			current_token = get_token()
		return None
	Node([current_token[0], current_token[1]], parent=node)
	u_token()

	StatementList(node)

	current_token = get_token()
	if current_token[0] != "end":
		errores()
		#FOLLOW(IfStatement) = ['break', 'continue', 'end', 'end.', 'for', 'id', 'if', 'write', 'writeln', '$']
		while current_token[0] not in ['break', 'continue', 'end', 'end.', 'for', 'id', 'if', 'write', 'writeln', '$']:
			u_token()
			current_token = get_token()
		return None
	Node([current_token[0], current_token[1]], parent=node)
	u_token()

	current_token = get_token()
	if current_token[0] != "PYCOM":
		errores()
		#FOLLOW(IfStatement) = ['break', 'continue', 'end', 'end.', 'for', 'id', 'if', 'write', 'writeln', '$']
		while current_token[0] not in ['break', 'continue', 'end', 'end.', 'for', 'id', 'if', 'write', 'writeln', '$']:
			u_token()
			current_token = get_token()
		return None
	Node([current_token[0], current_token[1]], parent=node)
	u_token()

	return None

def ForStatement(n_father):# ForStatement -> for id := Value to Expr do begin StatementList end ;
	current_token = get_token()
	if current_token[0] != "for":
		return None
	node = Node("ForStatement" , parent=n_father)
	Node([current_token[0], current_token[1]], parent=node)
	u_token()

	current_token = get_token()
	if current_token[0] != "id":
		errores()
		#FOLLOW(ForStatement) = ['break', 'continue', 'end', 'end.', 'for', 'id', 'if', 'write', 'writeln']
		while current_token[0] not in ['break', 'continue', 'end', 'end.', 'for', 'id', 'if', 'write', 'writeln','$']:
			u_token()
			current_token = get_token()
		return None
	Node([current_token[0], current_token[1]], parent=node)
	u_token()
	current_token = get_token()
	if current_token[0] != "ASIG":
		errores()
		#FOLLOW(ForStatement) = ['break', 'continue', 'end', 'end.', 'for', 'id', 'if', 'write', 'writeln']
		while current_token[0] not in ['break', 'continue', 'end', 'end.', 'for', 'id', 'if', 'write', 'writeln','$']:
			u_token()
			current_token = get_token()
		return None
	Node([current_token[0], current_token[1]], parent=node)
	u_token()

	Value(node)

	current_token = get_token()
	if current_token[0] != "to":
		errores()
		#FOLLOW(ForStatement) = ['break', 'continue', 'end', 'end.', 'for', 'id', 'if', 'write', 'writeln']
		while current_token[0] not in ['break', 'continue', 'end', 'end.', 'for', 'id', 'if', 'write', 'writeln','$']:
			u_token()
			current_token = get_token()
		return None
	Node([current_token[0], current_token[1]], parent=node)
	u_token()

	Expr(node)

	current_token = get_token()
	if current_token[0] != "do":
		errores()
		#FOLLOW(ForStatement) = ['break', 'continue', 'end', 'end.', 'for', 'id', 'if', 'write', 'writeln']
		while current_token[0] not in ['break', 'continue', 'end', 'end.', 'for', 'id', 'if', 'write', 'writeln','$']:
			u_token()
			current_token = get_token()
		return None
	Node([current_token[0], current_token[1]], parent=node)
	u_token()

	current_token = get_token()
	if current_token[0] != "begin":
		errores()
		#FOLLOW(ForStatement) = ['break', 'continue', 'end', 'end.', 'for', 'id', 'if', 'write', 'writeln']
		while current_token[0] not in ['break', 'continue', 'end', 'end.', 'for', 'id', 'if', 'write', 'writeln','$']:
			u_token()
			current_token = get_token()
		return None
	Node([current_token[0], current_token[1]], parent=node)
	u_token()

	StatementList(node)
	

	current_token = get_token()
	if current_token[0] != "end":
		errores()
		#FOLLOW(ForStatement) = ['break', 'continue', 'end', 'end.', 'for', 'id', 'if', 'write', 'writeln']
		while current_token[0] not in ['break', 'continue', 'end', 'end.', 'for', 'id', 'if', 'write', 'writeln','$']:
			u_token()
			current_token = get_token()
		return None
	Node([current_token[0], current_token[1]], parent=node)	
	u_token()

	current_token = get_token()
	if current_token[0] != "PYCOM":
		errores()
		#FOLLOW(ForStatement) = ['break', 'continue', 'end', 'end.', 'for', 'id', 'if', 'write', 'writeln']
		while current_token[0] not in ['break', 'continue', 'end', 'end.', 'for', 'id', 'if', 'write', 'writeln','$']:
			u_token()
			current_token = get_token()
		return None
	Node([current_token[0], current_token[1]], parent=node)
	u_token()

	return None

def Parse1():
	global root
	Program(root)
	if len(list_errores):
		return False
	return True

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
def printError():
	global list_errores
	for i in list_errores:
		print(i)