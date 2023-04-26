import re
import operation
import usf_types as types
import verify


strref = ' $strref"" '
strrefS = strref.strip()
bracref = ' $bracref '
bracrefS = bracref.strip()

def split_string(input_str):
    pattern = r'(\<-|\!=|\<|\>|\==|\//|\%|\,|\+|\-|\/|\*|\b(?:baye|ya|manz|chu)\b)'
    matches = re.findall(pattern, input_str)
    output_list = re.split(pattern, input_str)
    output_list = [s for s in output_list if s and s not in matches]
    return output_list, matches



def handle_brackets(expr):
    brac_index = 0
    output = ""
    substrs = []
    substr = ""
    in_quote = False
    for char in expr:
        if char == '(' and not in_quote:
            brac_index += 1
            if brac_index != 0: substr += char
        elif char == ')' and not in_quote:
            brac_index -= 1
            if brac_index == 0:
                output += bracref
                substrs.append(substr + ')')
                substr = ""
            else: substr += char
        else:
            if brac_index == 0:
                output += char
            else:
                substr += char
        if char == '"' : in_quote = not in_quote
    return output, substrs

def handle_strings(expr):
    pattern = r'"(.*?)"'
    output_str = re.sub(pattern, strref, expr)
    matches = re.findall(pattern, expr)
    return output_str, matches


def parse_array(function_caller,raw, *scopes):
    if raw.strip() == "": return types.ARRAY([])
    raw, bracs = handle_brackets(raw)
    raw, strings = handle_strings(raw)
    output = []
    for u in raw.split(","):
        while bracref in u:
            u = u.replace(bracrefS, bracs.pop(0), 1)
        while strref.strip() in u.strip():
            u = u.replace(strref.strip(), '"' + strings.pop(0) + '"', 1)
        output.append(collapse(function_caller, u, *scopes))
    return types.ARRAY(output)

def parse_arguments(function_caller,raw, *scopes):
    if raw.strip() == "": return []
    raw, bracs = handle_brackets(raw)
    raw, strings = handle_strings(raw)
    output = []
    for u in raw.split(","):
        while bracref in u:
            u = u.replace(bracrefS, bracs.pop(0), 1)
        while strref.strip() in u.strip():
            u = u.replace(strref.strip(), '"' + strings.pop(0) + '"', 1)
        output.append(collapse(function_caller, u, *scopes))
    return output

def parse_arguments_py(function_caller,raw, *scopes):
    if raw.strip() == "": return []
    raw, bracs = handle_brackets(raw)
    raw, strings = handle_strings(raw)
    output = []
    for u in raw.split(","):
        while bracref in u:
            u = u.replace(bracrefS, bracs.pop(0), 1)
        while strref.strip() in u.strip():
            u = u.replace(strref.strip(), '"' + strings.pop(0) + '"', 1)
        output.append(collapse(function_caller, u, *scopes).data)
    return output

def parse_object(function_caller, raw, *scopes):
    if raw.strip() == "": return types.DICT({})
    output = {}
    raw, bracs = handle_brackets(raw)
    raw, strings = handle_strings(raw)
    for u in raw.split(","):
        key, val = u.split(":", 1)
        while bracref in val:
            val = val.replace(bracrefS, bracs.pop(0), 1)
        while strref.strip() in val.strip():
            val = val.replace(strref.strip(), '"' + strings.pop(0) + '"', 1)
        output[key.strip()] = collapse(function_caller, val, *scopes)
    return types.DICT(output)

def get_from_scopes(var, scopes_in_order):
    verify.identifier(var)
    for scope in scopes_in_order:
        if var in scope: return scope[var]
    print("Failure: Variable " + var + " Was Not Found")
    exit()

def usf_range(mn, mx):
    output = []
    for n in range(mn, mxval):
        output.append(types.INTEGER(n))
    return output

def parse_f_string(function_caller, string, *scopes):
    string = re.split('\{|\}',string)
    output_str = ""
    for i, elem in enumerate(string):
        if not i % 2:
            output_str += elem
        else:
            output_str += str(collapse(function_caller, elem, *scopes).data)
    return output_str


def parse_unit(function_caller, u, strings, bracs,*scopes):
    stri = 0
    braci = 0
    if u.startswith(tuple("1234567890")):
        if u[-1] == 'N': u = '-' + u[0:-1]
        elif u[-1] == 'F' and "." not in u: u = u[0:-1] + '.0'
        elif u.endswith('F'): u = u[0:-1]
        if "." in u: return types.FLOAT(u)
        else: return types.INTEGER(u)
    elif u == strref.strip():
        return types.STRING(strings[stri])
        stri += 1
    elif u.startswith("@"):
        fn, val = tuple(u[1:].split(" ", 1))
        fn = fn.strip()
        if val.strip() == strref.strip():
            val = '"' + strings[stri] + '"'
            stri += 1
        while bracrefS in val:
            val = val.replace(bracrefS, bracs[braci], 1)
            braci += 1
        while strrefS in val:
            val = val.replace(strrefS, '"' + strings[stri] + '"', 1)
            stri += 1 
        if fn == "int":
            value = types.INTEGER(collapse(function_caller, val, *scopes).data)
        elif fn == "str":
            value = types.STRING(collapse(function_caller, val, *scopes).data)
        elif fn == "bool":
            value = types.BOOL(collapse(function_caller, val, *scopes).data)
        elif fn == "float":
            value = types.FLOAT(collapse(function_caller, val, *scopes).data)
        elif fn == "abs":
            value = types.INTEGER(abs(collapse(function_caller, val, *scopes).data))
        elif fn == "not":
            value = operation.NOT(collapse(function_caller, val, *scopes))
        elif fn == "typeof":
            value = types.STRING(collapse(function_caller, val, *scopes).type)
        elif fn == "len":
            value = types.INTEGER(len(collapse(function_caller, val, *scopes).data))
        elif fn == "input":
            value = types.STRING(input(collapse(function_caller, val, *scopes).data))
        return value
    elif u == bracrefS:
        u = bracs[braci][1:-1]
        if(u.startswith("[") and u.endswith("]")):
            return parse_array(function_caller, u[1:-1], *scopes)
        elif(u.startswith("{") and u.endswith("}")):
            return parse_object(function_caller, u[1:-1], *scopes)
        else:
            return collapse(function_caller, u, *scopes)
        braci += 1
    elif u.endswith(strrefS):
        if u.startswith("f"):
            return types.STRING(parse_f_string(function_caller, strings[stri], *scopes))
            stri += 1
    elif u in ["Apuz", "Poz"]:
        return types.BOOL(u == 'Poz')
    elif u == "none":
        return types.NONE()
    elif u.endswith(bracrefS):
        get_from = u.rsplit("$", 1)[0]
        while bracrefS in get_from:
            get_from = get_from.replace(bracrefS, bracs[braci], 1)
            braci += 1
        right = bracs[braci][1:-1]
        braci += 1
        if right.startswith(".."):
            right = collapse(function_caller, right[2:], *scopes)
            get_from = collapse(function_caller, get_from, *scopes)
            return types.auto(getattr(get_from.data, right.data))
        elif(right.startswith(".")):
            right = collapse(function_caller, right[1:], *scopes)
            get_from = collapse(function_caller, get_from, *scopes)
            return get_from.data[right.data]
        else:
            get_from = collapse(function_caller, get_from, *scopes)
            if type(get_from.data).__name__ == 'builtin_function_or_method':
                right = parse_arguments(function_caller, right, *scopes)
                return types.auto(get_from.data(*right))
            right = parse_arguments(function_caller, right, *scopes)
            return function_caller(get_from, *right)
    elif "." in u:
        left, key = u.rsplit(".", 1)
        # TODO
        left = collapse(function_caller, left, *scopes)
        return left.data[key]
    else:
       return get_from_scopes(u, scopes)

def stich(units, operators):
    i = -1
    for u in units:
        if i == -1:
            left = u
        else:
            if(operators[i] == "+"):
                left = operation.ADD(left, u)
            elif(operators[i] == "-"):
                left = operation.SUB(left, u)
            elif(operators[i] == "*"):
                left = operation.MUL(left, u)
            elif(operators[i] == "/"):
                left = operation.DIV(left, u)
            elif(operators[i] == "%"):
                left = operation.MOD(left, u)
            elif(operators[i] == "//"):
                left = operation.FLOOR_DIV(left, u)
            elif(operators[i] == "baye"):
                left = operation.AND(left, u)
            elif(operators[i] == "ya"):
                left = operation.OR(left, u)
            elif(operators[i] == "manz"):
                left = operation.IN(left, u)
            elif(operators[i] in ["==", "chu"]):
                left = operation.EQUALS(left, u)
            elif(operators[i] == "!="):
                left = operation.NOT_EQUALS(left, u)
            elif(operators[i] == "<"):
                left = operation.LLT(left, u)
            elif(operators[i] == ">"):
                left = operation.LGT(left, u)
            elif(operators[i] == "<-"):
                left.data.append(u)
        i += 1
    return left

def collapse(function_caller, expr, *scopes):
    units = []
    expr, bracs = handle_brackets(expr)
    expr, strings = handle_strings(expr)
    stri = 0
    braci = 0
    first_assign = True
    variables = scopes[0]
    if ":=" in expr:
        assign_to, expr = expr.split(":=", 1)
    elif "=:" in expr:
        assign_to, expr = expr.split("=:", 1)
        first_assign = False
    elif "+=" in expr:
        assign_to, expr = expr.split("+=", 1)
        expr = expr + " + " + assign_to
    elif "-=" in expr:
        assign_to, expr = expr.split("-=", 1)
        expr = expr + " - " + assign_to
    elif "*=" in expr:
        assign_to, expr = expr.split("*=", 1)
        expr = expr + " * " + assign_to
    elif "/=" in expr:
        assign_to, expr = expr.split("/=", 1)
        expr = expr + " / " + assign_to
    else:
        assign_to = None
    splitted_string, operators = split_string(expr)
    if assign_to != None:
        assign_to = assign_to.strip()
        verify.identifier(assign_to) 
    for u in splitted_string:
        units.append(parse_unit(function_caller, u.strip(), strings, bracs, *scopes))
    i = -1
    left = stich(units, operators)
    if assign_to :
        if first_assign: 
            variables[assign_to] = left
        else:
            left, variables[assign_to] = variables[assign_to], left
    return left