__author__  = "Diego Pellitero Fernández"
"""
Node: Class used for creating the binary tree
"""
class Node:

    def __init__(self, data, left, right=None):

        self.left = left
        self.right = right
        self.data = data


    def PrintTree(self):
        print("\t\t",self.data, "\n", self.left, "\t\t\t", self.right)


"""
Receives a sanitized list with the operations and builds the binary tree
"""
def create_tree(operations):
    while can_strip_parenthesis(operations):
        operations = strip_parenthesis(operations)
    index = lowest_priority_operation(operations)
    if index != -1:
        print("En la cadena ", operations, " el indice de menos prioridad es ", index)
        if index == 0:
             root = Node(operations[index], None, None)
        else:
            root = Node(operations[index], create_tree(operations[:index]), create_tree(operations[index + 1:]))
        return root
    else:
        return None
        

allowed_ops = {"+": 1, "-": 1, "*": 2, "/": 2, "**":3}
zerodivision = "div by 0"


#Receives a sanitized list with the operations and returns the index of the lowert priority
def lowest_priority_operation(_list):
    if len(_list) > 1:
        
        index_min = -1
        last_priority = 9999
        #use parenthesis variable to chech if an operatiuon is inside parenthesis
        parenthesis = 1
        #buscar operacion de menor prioridad
        for i in range(len(_list)):
            if _list[i] in allowed_ops:
                #ops inside parenthesis has more priority
                if (allowed_ops[_list[i]] * parenthesis) < last_priority:
                    index_min = i
                    last_priority = allowed_ops[_list[i]] * parenthesis
            else:
                if _list[i] == "(":
                    parenthesis *= 10
                elif _list[i] == ")":
                    parenthesis /= 10
        
        return index_min
    elif len(_list) == 1:
        return 0
    else: 
        return -1


def can_strip_parenthesis(_list):
    if _list[0] == "(" and _list[-1] == ")":
        count_par = 0
        for i in range(len(_list)):
            if _list[i] == "(":
                count_par += 1
            elif _list[i] == ")":
                count_par -= 1
                if count_par == 0:
                    if i == (len(_list) - 1):
                        return True
                    else:
                        return False
                
    else: return False

def strip_parenthesis(_list):
    return _list[1:-1]

def solve_op(op, left_op, right_op):
    if op == "+":
        result = left_op + right_op
    elif op == "-":
        result = left_op - right_op
    elif op == "*":
        result = left_op * right_op
    elif op == "/":
        try:
            result = left_op / right_op
        except:
            return zerodivision
    elif op == "**":
        result = left_op ** right_op
    return result


def solve_tree(_root):
    print("Operacion: ", _root.data, end=" ")
    if _root.left == None and _root.right == None:
        return _root.data
    if _root.left.data in allowed_ops:
        left_op = solve_tree(_root.left)

        print("Left: ", _root.left.data, end=" ")

    else:
        left_op = _root.left.data

        print("Left: ", _root.left.data, end=" ")

    if _root.right.data in allowed_ops:
        right_op = solve_tree(_root.right)

        print("right: ", _root.right.data, end=" ")

    else: 
        right_op = _root.right.data

        print("right: ", _root.right.data)

    if left_op == zerodivision or right_op == zerodivision:
        return zerodivision
    else:
        result = solve_op(_root.data, left_op, right_op)
        return result





def printNodes(node):
    print(node.data)
    if node.left != None:
        printNodes(node.left)
    if node.right != None:
        printNodes(node.right)

def count_parenthesis(lista):
    count = 0
    for element in lista:
        if element == "(":
            count += 1
        elif element == ")":
            count -= 1
    return count

def solve(lista):
    if count_parenthesis(lista):
        return "Cuenta mal formada, comprueba los parentesis"
    root_node = create_tree(lista)
    return solve_tree(root_node)

"""
***************************************************

Aqui añado lo nuevo de menú

***************************************************
"""


def print_menu():
    print("\n")
    menu = """Bienvenido a la calculadora
    \nLas operaciones permitidas son:
    \tsuma("+")
    \tresta("-")
    \tmultiplicacion("*")
    \tdivision ("/")
    \texponenciales("**")
    \traices cuadradas("sqrt")
    Esta calculadora soporta operaciones compuestas y parentesis, ademas, respeta las prioridades de las operaciones"""
    print(menu)

def print_operations():
    cad="""Elija una operación:
    \t+. Suma
    \t-. Resta
    \t*. Muliplicación
    \t/. División
    \t**. Potencia"""
    if parenthesis_num > 0:
        cad = cad + "\n\t\")\". Cierre parentesis"
    if in_sqrt:
        cad = cad + "\n\tfin. Salir de raiz"
    if parenthesis_num == 0 and not in_sqrt:
        cad = cad + "\n\t=. Calcular"
    print(cad)



def get_operator():
    while True:
        op = input("Introduce la operacion: ")
        if op in allowed_ops or op == ")":
            return op
        elif op == "=" and not in_sqrt and parenthesis_num == 0:
            return op
        elif in_sqrt and op == "fin":
            return op
        else:
            print("Operacion no valida")

def get_number():
    while True:
        try:
            if last_result != None and not in_sqrt:
                cad = ("Introduce un numero, un simbolo de parentesis, sqrt para una raiz cuadrada o \"r\" para usar el resultado anterior: ")
            elif last_result != None and in_sqrt:
                cad = ("Introduce un numero, un simbolo de parentesis o \"r\" para usar el resultado anterior: ")
            elif in_sqrt:
                cad = ("Introduce un numero o un simbolo de parentesis: ")
            else:
                cad = ("Introduce un numero o un simbolo de parentesis o sqrt para una raiz cuadrada: ")
            num1 = input(cad)
            if num1 == "r" and last_result != None:
                return last_result
            if num1 == "(":
                return num1
            elif num1 == "sqrt" and not in_sqrt:
                return num1
            else:
                num1 = float(num1)
                return num1
            break
        except ValueError:
            print("Numero invalido, introduce un numero (usa el punto \".\" como separacion decimal)")

def append_sqrt(radicando):
    global visual_op
    global regular_op
    visual_op.append("√(")
    visual_op += radicando
    visual_op.append(")")
    radicando.insert(0, "(")
    radicando += [")", "**", 0.5]
    regular_op += radicando
    return radicando

def sqrt_maker():
    radicando = []
    print("\n\nIntroduce el radicando de la raiz cuadrada (no se permites raices anidadas): \n")

    while True:
        while True:
            num = get_number()
            
            if num == "(":
                radicando.append(num)
                for i in radicando:
                    print(i, end=" ")
                print()
            else:
                radicando.append(num)
                for i in radicando:
                    print(i, end=" ")
                print()
                break
            
        while True:
            print_operations()
            op = get_operator()
            if op == "fin":
                
                return radicando
            elif op == ")":
                radicando.append(op)
                for i in radicando:
                    print(i, end=" ")
                print()
            else:
                radicando.append(op)
                for i in radicando:
                    print(i, end=" ")
                print()
                break

    
#Here starts the program
end = False
last_result = None
in_sqrt = False

print_menu()
input("Para comenzar una operacion pulse cualquier tecla")
while not end:
    print("\nNueva operacion")
    parenthesis_num = 0
    visual_op = []
    regular_op = []

    
    while True:
        
        #Add number, and if its a parenthesis, let the user add another number
        while True:
            num = get_number()
            if num == "sqrt":
                in_sqrt = True
                num = sqrt_maker()
                in_sqrt = False
                append_sqrt(num)
            else:
                visual_op.append(num)
                regular_op.append(num)
            print()
            for i in visual_op:
                print(i, end=" ")
            print("")
            if num != "(":
                break
            else:
                parenthesis_num += 1


        #Add operation
        while True:
            print_operations()
            operation = get_operator()
            if operation == "=":
                visual_op.append(operation)
                break
            elif operation == ")":
                parenthesis_num -= 1
                visual_op.append(operation)
                regular_op.append(operation)
            else:
                visual_op.append(operation)
                regular_op.append(operation)
                break
        if operation == "=":
            break
        print()
        for i in visual_op:
            print(i, end=" ")
        print()
    for i in visual_op:
        print(i, end=" ")
    result = solve(regular_op)
    print(result)
    if result != zerodivision:
        last_result = result
    ##calcular el resultado aquí
    next = input("Si desea realizar otra operacion pulse s, de lo contrario pulse cualquier otra letra: ")
    if(next.lower() != "s"):
        end = True


print("Gracias por usar mi calculadora, vuelva pronto!")

