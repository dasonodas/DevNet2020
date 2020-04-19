__author__  = "Diego Pellitero Fernández"
"""
Node: Class used for creating the binary tree
"""
class Node:

    def __init__(self, data, left, right=None):

        self.left = left
        self.right = right
        self.data = data


    def PrintNode(self):
        print("\t\t",self.data, "\n", self.left, "\t\t\t", self.right)


"""
Receives a list with the operations and builds the binary tree
"""
def create_tree(operations):
    while can_strip_parenthesis(operations):
        operations = strip_parenthesis(operations)
    index = lowest_priority_operation(operations)
    if index != -1:
        #print("En la cadena ", operations, " el indice de menos prioridad es ", index)
        if index == 0:
             root = Node(operations[index], None, None)
        else:
            root = Node(operations[index], create_tree(operations[:index]), create_tree(operations[index + 1:]))
        return root
    else:
        return None
        

allowed_ops = {"+": 1, "-": 1, "*": 2, "/": 2, "**":3}
zerodivision = "div by 0"

"""
Receives list with the operations and returns the index of the lowert priority
"""
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

"""
Check if can get rid of parenthesis on the sides
"""
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

"""
If a list is bounded by parenthesis and can_strip_parenthesis, get rid of them
"""
def strip_parenthesis(_list):
    return _list[1:-1]

"""
Solve a simple operation
"""
def solve_op(op, left_op, right_op):
    try:
        if op == "+":
            result = left_op + right_op
        elif op == "-":
            result = left_op - right_op
        elif op == "*":
            result = left_op * right_op
        elif op == "/":
                result = left_op / right_op
        elif op == "**":
            result = left_op ** right_op
    except:
            raise

    return result

"""
Takes a tree as argument and start resolving from the left side
"""
def solve_tree(_root):
    #Check if _root is a leaf node
    if _root.left == None and _root.right == None:
        return _root.data
    try:
        #If left child is operation, solve it
        if _root.left.data in allowed_ops:
            left_op = solve_tree(_root.left)
        else:
            left_op = _root.left.data

        #If left child is operation, solve it
        if _root.right.data in allowed_ops:
            right_op = solve_tree(_root.right)
        else: 
            right_op = _root.right.data
    except:
        raise

    else:
        result = solve_op(_root.data, left_op, right_op)
        return result

"""
Print tree, for debug only
"""
def printNodes(node):
    print(node.data)
    if node.left != None:
        printNodes(node.left)
    if node.right != None:
        printNodes(node.right)

"""
Take a list as argument and checks if the parenthesis match
"""
def count_parenthesis(lista):
    count = 0
    for element in lista:
        if element == "(":
            count += 1
        elif element == ")":
            count -= 1
    return count

"""
Takes a list as argument and solve it
"""
def solve(lista):
    if count_parenthesis(lista):
        return "Cuenta mal formada, comprueba los parentesis"
    root_node = create_tree(lista)
    try:
        return solve_tree(root_node)
    except:
        raise

"""
Prints welcome menu
"""
def print_menu():
    print("\n")
    menu = """***********************************
*   Bienvenido a la calculadora   *
***********************************
    \nLas operaciones permitidas son:
    \tSuma("+")
    \tResta("-")
    \tMultiplicacion("*")
    \tDivision ("/")
    \tExponenciales("**")
    \tRaices cuadradas("sqrt")
    \nEsta calculadora soporta operaciones compuestas y parentesis, ademas, respeta las prioridades de las operaciones\n\n"""
    print(menu)

"""
Prints allowed ops on each moment
"""
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

"""
Gets the input of a user and check if its a valid operation, then returns it
"""
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

"""
Gets the input of a user and check if its a valid number or ( or sqrt, then returns it
"""
def get_number():
    while True:
        try:
            if last_result != None and not in_sqrt:
                cad = ("Introduce un numero, un simbolo de parentesis \"(\", \"sqrt\" para una raiz cuadrada o \"r\" para usar el resultado anterior: ")
            elif last_result != None and in_sqrt:
                cad = ("Introduce un numero, un simbolo de parentesis \"(\" o \"r\" para usar el resultado anterior: ")
            elif in_sqrt:
                cad = ("Introduce un numero o un simbolo de parentesis: ")
            else:
                cad = ("Introduce un numero o un simbolo de parentesis \"(\" o \"sqrt\" para una raiz cuadrada: ")
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

"""
Takes the end list of the sqrt and generate a beautiful one and appends the ops
"""
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

"""
Gets the ops inside an sqrt
"""
def sqrt_maker():
    radicando = []
    print("\n\nIntroduce el radicando de la raiz cuadrada (no se permiten raices anidadas): \n")

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
#End variable as flag for main loop
#last_result stores the result of the last operacion
#in_sqrt flag to know that we are inside a sqrt operation
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
            for i in visual_op:
                print(i, end=" ")
            print()
            num = get_number()
            if num == "sqrt":
                in_sqrt = True
                num = sqrt_maker()
                in_sqrt = False
                append_sqrt(num)
            else:
                visual_op.append(num)
                regular_op.append(num)
            
            
            if num != "(":
                break
            else:
                parenthesis_num += 1

        #Add operation
        while True:
            print_operations()
            for i in visual_op:
                print(i, end=" ")
            print()
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
        """for i in visual_op:
            print(i, end=" ")
        print()"""
    for i in visual_op:
        print(i, end=" ")

    #Once the user ends the input, calculate the result
    print("\n\n**************************\n")
    for i in visual_op:
            print(i, end=" ")
    try:
        result = solve(regular_op)
        print()
        print('\033[92m' ,result, '\033[0m')
        print()
    except ZeroDivisionError:
        print("\033[91mError, division por 0\033[0m")
    except:
        print("\033[91mError no contemplado\033[0m")
    print("\n**************************\n")

    next = input("Si desea realizar otra operacion pulse s, de lo contrario pulse cualquier otra letra: ")
    if(next.lower() != "s"):
        end = True


print("\nGracias por usar mi calculadora, vuelva pronto!\n")