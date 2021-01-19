# Analizador sintactico
from Lexico import lexico
from Semantico import semantico
import master
from master import Token, Simbolo, Tabla_Simbolos


# ATRIBUTES
global file_lines, sig_token, parse

parse = []
master.token_list = []
master.tablas_simbolos = {}

# FUNCTIONS


def analizador(file_path):
    """
    Recibe una liena como entrada del analizador general y hace la generacion del arbol
    Manda al analizador semantico el arbol para que este lo analice y anyada atributos
    Pide uno a uno los tokens al analizador lexico
    """
    global file_lines, sig_token

    with open(file_path, 'r') as file:
        file_lines = file.readlines()

    # Obtiene el primer token
    sig_token = pedir_token()
    # llama al estado inicial
    P(Simbolo(lexema=None))

    return parse, master.token_list, master.tablas_simbolos


def pedir_token():
    """
    se encarga de recorrer los elementos del fichero de entrada
    y llamar a la funcion get_token del analizador lexico
    """
    global file_lines, sig_token

    if file_lines:
        master.last_line = True if len(file_lines) == 1 else False

        file_lines[0], token = lexico.get_token(file_lines[0])

        if token == 'null':
            token = pedir_token()

        elif token.key == 'final' and token.value == 'eol':
            file_lines = file_lines[1:]
            master.line_count += 1
            token = pedir_token()

    return token


def error_parse(token):
    # Cambiarlo en funcion de la correccion
    with open(master.file_paths["error"], 'w') as error_file:
        message = 'Error sintactico: '+token.value + \
            ', en linea: '+str(token.linea)+'\n'
        error_file.write(message)
    exit()


# Una función para cada no terminal (y una rama para cada regla)
# Hacer las llamadas al sematico cuando corresponda


def equipara(valor):
    global sig_token

    if 'ID' == valor == sig_token.key:
        sig_token = pedir_token()
    elif 'whole_const' == valor == sig_token.key:
        sig_token = pedir_token()
    elif 'chain' == valor == sig_token.key:
        sig_token = pedir_token()
    elif sig_token.value == valor:
        sig_token = pedir_token()
    else:
        error_parse(Token('equipara', 'error', master.line_count))

    master.token_list.append(sig_token)

# Una función para cada no terminal (y una rama para cada regla)


def E(simbolo):

    valor = sig_token.value

    if valor == 'not' or valor == 'open_par' or sig_token.key == 'chain' or sig_token.key == 'whole_const' or valor == 'false' or sig_token.key == 'ID' or valor == 'true':
        parse.append(1)
        # (not or open_par or chain or whole_const or ...) R E1
        simbolo = R(simbolo)
        simbolo = E1(simbolo)
    else:
        error_parse(sig_token)

    return simbolo


def E1(simbolo):
    valor = sig_token.value

    if valor == 'and':
        parse.append(2)
        # && R E1
        equipara('and')
        simbolo = R(simbolo)
        simbolo = E1(simbolo)
    # FOLLOW de E1  =  { ) , ; }
    elif valor == 'close_par' or valor == 'colon' or valor == 'semicolon':
        parse.append(3)
    else:
        error_parse(sig_token)

    return simbolo


def R(simbolo):

    valor = sig_token.value

    if valor == 'not' or valor == 'open_par' or sig_token.key == 'chain' or sig_token.key == 'whole_const' or valor == 'false' or sig_token.key == 'ID' or valor == 'true':
        parse.append(4)
        # (not or open_par or ...) U R1
        simbolo = U(simbolo)
        simbolo = R1(simbolo)
    else:
        error_parse(sig_token)

    return simbolo


def R1(simbolo):

    valor = sig_token.value

    if valor == 'equals':
        parse.append(5)
        # == U R1
        equipara('equals')
        simbolo = U(simbolo)
        simbolo = R1(simbolo)
    elif valor == 'not_equals':
        parse.append(6)
        # != U R1
        equipara('not_equals')
        simbolo = U(simbolo)
        simbolo = R1(simbolo)
    elif valor == 'and' or valor == 'close_par' or valor == 'colon' or valor == 'semicolon':
        parse.append(7)
    else:
        error_parse(sig_token)

    return simbolo


def U(simbolo):

    valor = sig_token.value

    if valor == 'not' or valor == 'open_par' or sig_token.key == 'chain' or sig_token.key == 'whole_const' or valor == 'false' or sig_token.key == 'ID' or valor == 'true':
        parse.append(8)
        # (not or open_par or ...) V U1
        simbolo = V(simbolo)
        simbolo = U1(simbolo)
    else:
        error_parse(sig_token)

    return simbolo


def U1(simbolo):

    valor = sig_token.value

    if valor == 'plus':
        parse.append(9)
        # + V U1
        equipara('plus')
        simbolo = V(simbolo)
        simbolo = U1(simbolo)
    elif valor == 'minus':
        parse.append(10)
        # - V U1
        equipara('minus')
        simbolo = V(simbolo)
        simbolo = U1(simbolo)
    elif valor == 'not_equals' or valor == 'and' or valor == 'close_par' or valor == 'colon' or valor == 'semicolon' or valor == 'equals':
        parse.append(11)
    else:
        error_parse(sig_token)

    return simbolo


def V(simbolo):

    valor = sig_token.value

    if sig_token.key == 'ID':
        parse.append(12)
        # ID V1
        equipara('ID')
        simbolo = V1(simbolo)
    elif valor == 'open_par':
        parse.append(13)
        # ( E )
        equipara('open_par')
        simbolo = E(simbolo)
        equipara('close_par')
    elif sig_token.key == 'whole_const':
        parse.append(14)
        # whole_const
        equipara('whole_const')
        simbolo = Simbolo('hacer semantico aqui')
    elif sig_token.key == 'chain':
        parse.append(15)
        # chain
        equipara('chain')
        simbolo = Simbolo('hacer semantico aqui')
    elif valor == 'true':
        parse.append(16)
        # true
        equipara('true')
        simbolo = Simbolo('hacer semantico aqui')
    elif valor == 'false':
        parse.append(17)
        # false
        equipara('false')
        simbolo = Simbolo('hacer semantico aqui')
    elif valor == 'not':
        parse.append(18)
        # not ID
        equipara('not')
        equipara('ID')
        simbolo = Simbolo('hacer semantico aqui')

    return simbolo


def V1(simbolo):

    valor = sig_token.value

    if valor == 'open_par':
        parse.append(19)
        # ( L )
        equipara('open_par')
        simbolo = L(simbolo)
        equipara('close_par')
    elif valor == 'auto_inc':
        parse.append(20)
        # ++
        equipara('auto_inc')
    elif valor == 'not_equals' or valor == 'and' or valor == 'close_par' or valor == 'plus' or valor == 'colon' or valor == 'minus' or valor == 'semicolon' or valor == 'equals':
        parse.append(21)
    else:
        error_parse(sig_token)

    return simbolo


def S(simbolo):

    valor = sig_token.value

    if sig_token.key == 'ID':
        parse.append(22)
        # ID S1
        equipara('ID')
        simbolo = S1(simbolo)
    elif valor == 'alert':
        parse.append(23)
        # alert ( E ) ;
        equipara('alert')
        equipara('open_par')
        simbolo = E(simbolo)
        equipara('close_par')
        equipara('semicolon')
    elif valor == 'input':
        parse.append(24)
        # input ( ID ) ;
        equipara('input')
        equipara('open_par')
        equipara('ID')
        equipara('close_par')
        equipara('semicolon')
    elif valor == 'return':
        parse.append(25)
        # return X ;
        equipara('return')
        simbolo = X(simbolo)
        equipara('semicolon')
    else:
        error_parse(sig_token)

    return simbolo


def S1(simbolo):

    valor = sig_token.value

    if valor == 'equal':
        parse.append(26)
        # = E ;
        equipara('equal')
        simbolo = E(simbolo)
        equipara('semicolon')
    elif valor == 'open_par':
        parse.append(27)
        # ( L ) ;
        equipara('open_par')
        simbolo = L(simbolo)
        equipara('close_par')
        equipara('semicolon')
    elif valor == 'auto_inc':
        # ++ ;
        equipara('auto_inc')
        equipara('semicolon')
    else:
        error_parse(sig_token)

    return simbolo


def L(simbolo):

    valor = sig_token.value

    if valor == 'not' or valor == 'open_par' or sig_token.key == 'chain' or sig_token.key == 'whole_const' or valor == 'false' or sig_token.key == 'ID' or valor == 'true':
        parse.append(28)
        # (not or open_par or ...) E Q
        simbolo = E(simbolo)
        simbolo = Q(simbolo)
    elif valor == 'close_par':
        parse.append(29)
    else:
        error_parse(sig_token)

    return simbolo


def Q(simbolo):

    valor = sig_token.value

    if valor == 'colon':
        parse.append(30)
        # , E Q
        equipara('colon')
        simbolo = E(simbolo)
        simbolo = Q(simbolo)
    elif valor == 'close_par':
        parse.append(31)
    else:
        error_parse(sig_token)

    return simbolo


def X(simbolo):

    valor = sig_token.value

    if valor == 'not' or valor == 'open_par' or sig_token.key == 'chain' or sig_token.key == 'whole_const' or valor == 'false' or sig_token.key == 'ID' or valor == 'true':
        parse.append(32)
        # (not or open_par or ...) E
        simbolo = E(simbolo)
    elif valor == 'semicolon':
        parse.append(33)
    else:
        error_parse(sig_token)

    return simbolo


def B(simbolo):

    valor = sig_token.value

    if valor == 'if':
        parse.append(34)
        # if ( E ) S
        equipara('if')
        equipara('open_par')
        simbolo = E(simbolo)
        equipara('close_par')
        simbolo = S(simbolo)

    elif valor == 'let':
        parse.append(35)
        # let T ID ;
        equipara('let')
        simbolo = T(simbolo)
        equipara('ID')
        equipara('semicolon')

    elif valor == 'alert' or sig_token.key == 'ID' or valor == 'input' or valor == 'return':
        parse.append(36)
        # (alert or ID or input or return) S
        simbolo = S(simbolo)

    elif valor == 'do':
        parse.append(37)
        # do { C } while ( E );
        equipara('do')
        equipara('open_braq')
        simbolo = C(simbolo)
        equipara('close_braq')
        equipara('while')
        equipara('open_par')
        simbolo = E(simbolo)
        equipara('close_par')
        equipara('semicolon')
    else:
        error_parse(sig_token)

    return simbolo


def T(simbolo):

    valor = sig_token.value

    if valor == 'number':
        parse.append(38)
        equipara('number')
        simbolo = Simbolo('SEMANTICO')
    elif valor == 'boolean':
        parse.append(39)
        equipara('boolean')
        simbolo = Simbolo('SEMANTICO')
    elif valor == 'string':
        parse.append(40)
        equipara('string')
        simbolo = Simbolo('SEMANTICO')
    else:
        error_parse(sig_token)

    return simbolo


def F(simbolo):

    valor = sig_token.value

    if valor == 'function':
        parse.append(41)
        # function H ID ( A ) { C }
        equipara('function')
        simbolo = H(simbolo)
        equipara('ID')
        equipara('open_par')
        simbolo = A(simbolo)
        equipara('close_par')
        equipara('open_braq')
        simbolo = C(simbolo)
        equipara('close_braq')
        # SEMANTICO Y CREAR TABLA DE SIMBOLOS
    else:
        error_parse(sig_token)

    return simbolo


def H(simbolo):

    valor = sig_token.value

    if valor == 'boolean' or valor == 'number' or valor == 'string':
        parse.append(42)
        # (boolean or number or string) T
        simbolo = T(simbolo)
    elif sig_token.key == 'ID':
        parse.append(43)
    else:
        error_parse(sig_token)

    return simbolo


def A(simbolo):

    valor = sig_token.value

    if valor == 'boolean' or valor == 'number' or valor == 'string':
        parse.append(44)
        # (boolean or number or string ) T ID K
        simbolo = T(simbolo)
        equipara('ID')
        simbolo = K(simbolo)
    elif valor == 'close_par':
        parse.append(45)
    else:
        error_parse(sig_token)

    return simbolo


def K(simbolo):

    valor = sig_token.value

    if valor == 'colon':
        parse.append(46)
        # , T ID K
        equipara('colon')
        simbolo = T(simbolo)
        equipara('ID')
        simbolo = K(simbolo)
    elif valor == 'close_par':
        parse.append(47)
    else:
        error_parse(sig_token)

    return simbolo


def C(simbolo):

    valor = sig_token.value

    if valor == 'alert' or valor == 'do' or sig_token.key == 'ID' or valor == 'if' or valor == 'input' or valor == 'let' or valor == 'return':
        parse.append(48)
        # ( alert or do or ... ) B C
        simbolo = B(simbolo)
        simbolo = C(simbolo)
    elif valor == 'close_braq':
        parse.append(49)
    else:
        error_parse(sig_token)

    return simbolo


def P(simbolo):

    valor = sig_token.value

    if valor == 'alert' or valor == 'do' or sig_token.key == 'ID' or valor == 'if' or valor == 'input' or valor == 'let' or valor == 'return':
        parse.append(50)
        simbolo = B(simbolo)
        simbolo = P(simbolo)
    elif valor == 'function':
        parse.append(51)
        simbolo = F(simbolo)
        simbolo = P(simbolo)
    elif valor == '$':
        parse.append(52)
        # hemos terminado
        # habra que añadir a TL un dolar al final para saber que hemos acabado el archivo
    else:
        error_parse(sig_token)

    return simbolo
