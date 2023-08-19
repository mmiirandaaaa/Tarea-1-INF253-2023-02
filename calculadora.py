import re

ans = 0

# EBNF

entero = r'[1-9][0-9]*|0'
operacion = r'(?P<num1>[1-9][0-9]*|0)\s*(?P<operando>[-*+]|//)\s*(?P<num2>[1-9][0-9]*|0)'
multdiv = r'(?P<num1>[1-9][0-9]*|0)\s*(?P<operando>[*]|//)\s*(?P<num2>[1-9][0-9]*|0)'
suma_resta = r'(?P<num1>[1-9][0-9]*|0)\s*(?P<operando>[-+])\s*(?P<num2>[1-9][0-9]*|0)'
clave = r'ANS|CUPON\(\s*(?P<x>'+'|'.join([entero,'ANS'])+r')\s*(?:,\s*(?P<y>'+'|'.join([entero,'ANS'])+r')\s*)?\)'

# REGEX

entero_regex = re.compile(entero)
mult_div_regex = re.compile(multdiv)
sum_rest_regex = re.compile(suma_resta)
clave_regex = re.compile(clave)
parentesis_regex = re.compile(r'\(')

# REPLACE FUNCTIONS

def replace_claves(matchobj):
	'''
	***
	* matchobj : Match Object
	***
	Función auxiliar del método sub. 
	Reemplaza las claves por su valor numerico
	'''
	if matchobj.group() == 'ANS':
		return str(ans)
	else:
		if matchobj['x'] == 'ANS':
			x = ans
		else:
			x = int(matchobj['x'])

		if matchobj['y']:
			if matchobj['y'] == 'ANS':
				y = ans
			else:
				y = int(matchobj['y'])
			return str(int(x*y/100))
		else:
			return str(int(x*0.2))

def replace_mult_y_div(matchobj):
	'''
	***
	* matchobj : Match Object
	***
	Función auxiliar del método sub.
	Reemplaza los patrones (entero (*|//) entero) por el valor
	obtenido de realizar la operacion dada. Si se intenta
	dividir por 0 se coloca la palabra ERROR en lugar de la operación.
	'''
	if matchobj['operando'] == '*':
		result = int(matchobj['num1'])*int(matchobj['num2'])
		return str(result)
	else:
		if matchobj['num2'] == '0':
			return 'ERROR'
		result = int(matchobj['num1'])//int(matchobj['num2'])
		return str(result)

def replace_suma_y_resta(matchobj):
	'''
	***
	* matchobj : Match Object
	***
	Función auxiliar del método sub.
	Reemplaza los patrones (entero (+|-) entero) por el valor
	obtenido de realizar la operacion dada. Si el resultado de
	la operación da negativo se coloca un 0 en su lugar.
	'''
	if matchobj['operando'] == '+':
		result = int(matchobj['num1'])+int(matchobj['num2'])
		if result < 0:
			result = 0
		return str(result)
	else:
		result = int(matchobj['num1'])-int(matchobj['num2'])
		if result < 0:
			result = 0
		return str(result)


# RESOLVER FUNCTIONS

def resolver_parentesis(string):
	'''
	***
	* string : string
	***
	Busca el paréntesis más grande que encuentre y retorna el string recibido pero
	reemplazando el paréntesis más grande por el valor de realizar la operación dentro
	de ese paréntesis.
	'''
	abierto = 0
	if parentesis_regex.search(string):
		abre = pos = parentesis_regex.search(string).start()
	else:
		return string

	while pos < len(string):
		if string[pos] == '(':
			abierto+=1
		elif string[pos] == ')':
			abierto-=1

		if abierto == 0:
			break
		pos+=1
	if entero_regex.fullmatch(string[abre+1:pos]):
		return 'ERROR'
	if abierto != 0:
		return 'ERROR'
	else:
		return string[:abre] + resolver(string[abre+1:pos]) + string[pos+1:]

def resolver_claves(string):
	'''
	***
	* string : string
	***
	Recibe una sentencia de calculadora, busca todas las claves presentes
	y luego reemplaza las claves por el valor numerico que representan.
	Retorna el string con las claves reemplazadas.
	'''
	while clave_regex.search(string):
		string = clave_regex.sub(replace_claves, string)
	return string

def resolver_mult_y_div(string):
	'''
	***
	* string : string
	***
	Busca todas las multiplicaciones y divisiones (entero (*|//) entero)
	en el string recibido y las resuelve, luego coloca ese valor en lugar
	de la operacion y retorna el string resultante
	'''
	while mult_div_regex.search(string):
		string = mult_div_regex.sub(replace_mult_y_div, string)
	return string

def resolver_suma_y_resta(string):
	'''
	***
	* string : string
	***
	Análoga al funcionamiento de la función resolver_mult_div
	pero para la suma y resta
	'''
	while sum_rest_regex.search(string):
		string = sum_rest_regex.sub(replace_suma_y_resta, string)
	return string

def resolver(string):
	'''
	***
	* string : string
	***
	Recibe una sentencia de calculadora. Resuelve las claves, luego
	resuelve los parentesis, y finalmente resuelve las multiplicaciones
	y divisiones y sumas y restas restantes. Retorna el string resultante
	de realizar esas operaciones sobre la sentencia recibida.
	Si la sentencia resultante termina NO siendo un número, o teniendo
	la palabra ERROR en ella esto quiere decir que hubo un error en la sintáxis.
	Por lo que retorna ERROR.
	'''
	string = resolver_claves(string)

	while parentesis_regex.search(string):
		string = resolver_parentesis(string)
	string = resolver_mult_y_div(string)
	string = resolver_suma_y_resta(string)
	if ('ERROR' in string) or (not entero_regex.fullmatch(string)):
		return 'ERROR'
	global ans
	ans = int(string)
	return string

#MAIN PROGRAM

entrada = open('problemas.txt','r')
salida = open('desarrollos.txt','w')
resultados = {}
error_flag = False

for linea in entrada:
	linea = linea.strip()
	if linea == '':
		if error_flag:
			for problema in resultados:
				if resultados[problema] == 'ERROR':
					salida.write(problema + ' = ' + resultados[problema] + '\n')
				else:
					salida.write(problema + ' = ' + 'Sin Resolver' + '\n')
			salida.write('\n')
			error_flag = False
			ans = 0
			resultados.clear()

		else:
			for problema in resultados:
				salida.write(problema + ' = ' + resultados[problema] + '\n')
			salida.write('\n')
			ans = 0
			resultados.clear()
	else:
		solved = resolver(linea)
		if solved == 'ERROR':
			error_flag = True
		resultados[linea] = solved

for problema in resultados:
	salida.write(problema + ' = ' + resultados[problema] + '\n')

entrada.close()
salida.close()