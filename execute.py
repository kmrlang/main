import expr
import usf_types as types
import parsecode
import printer

conditionals_info = {}

variables = {}

break_loop = False
continue_loop = False
return_value_switch = False
return_value = None

def match_keyword(value, *keywords):
    return value in keywords

def repeat(line_body, block, scopes):
    global break_loop, continue_loop
    parsed_block = parsecode.parse_block(block)
    limit = expr.collapse(call_function, line_body[:-1], *scopes).data
    scopes = [scopes[0]] if len(scopes) == 2 else []
    for i in range(0, limit):
        block_id = __get_next_bid()
        conditionals_info[block_id] = {
            "was_last_conditional" : False,
            "last_condition_status": False
        }
        for instruction in parsed_block:
            execute(*instruction, bid = block_id, scopes = scopes)
            if(break_loop):
                break_loop = False
                return
            elif(continue_loop):
                continue_loop = False
                break
            if return_value_switch: return
        del conditionals_info[block_id]

def create_sub(line_body, block, variables):
    name, arguments = line_body.split("(", 1)
    name = name.strip()
    arguments = arguments[:-2].split(",")
    variables[name] = types.FUNCTION(block, arguments)

def while_loop(line_body, block, scopes):
    global break_loop, continue_loop
    condition = line_body[:-1]
    parsed_block = parsecode.parse_block(block)
    scopes = [scopes[0]] if len(scopes) == 2 else scopes
    while expr.collapse(call_function, condition, *scopes).data: 
        block_id = __get_next_bid()
        conditionals_info[block_id] = {
            "was_last_conditional" : False,
            "last_condition_status": False
        }
        for instruction in parsed_block:
            execute(*instruction, bid = block_id, scopes = scopes)
            if(break_loop):
                break_loop = False
                return
            elif(continue_loop):
                continue_loop = False
                break
            if return_value_switch: return
        del conditionals_info[block_id]

def if_statement(line_body, block, bid, scopes):
    global conditionals_info
    condition = expr.collapse(call_function, line_body[:-1], *scopes).data
    conditionals_info[bid]["was_last_conditional"] = True
    conditionals_info[bid]["last_condition_status"] = condition
    if not condition: return
    execute_block(block, scopes)

def else_statement(line_body, block, bid, scopes):
    global conditionals_info
    if not conditionals_info[bid]["was_last_conditional"]:
        print("Nothing To Associate This With")
        return
    if not conditionals_info[bid]["last_condition_status"]:
        execute_block(block, scopes)
    conditionals_info[bid]["was_last_conditional"] = False

def elseif_statement(line_body, block, bid, scopes):
    global conditionals_info
    if not conditionals_info[bid]["was_last_conditional"]:
        print("Nothing To Associate This With")
        return
    condition = expr.collapse(call_function, line_body[:-1], *scopes).data
    if not conditionals_info[bid]["last_condition_status"]:
        if condition:
            execute_block(block, scopes)
            conditionals_info[bid]["last_condition_status"] = condition

block_id = -1

def execute(keyword, line_body, block, bid, scopes = []):
    global break_loop, continue_loop, return_value_switch, return_value
    variables["bid"] = types.INTEGER(bid)
    scopes = [*scopes, variables]
    if match_keyword(keyword, "wan"):
        printer.usf_print(expr.collapse(call_function, line_body, *scopes))
    elif match_keyword(keyword, "wan_niloey"):
        printer.usf_print_raw(expr.collapse(call_function, line_body, *scopes))
    elif match_keyword(keyword, "#"):
        pass
    elif match_keyword(keyword, "rozkaran"):
        repeat(line_body, block, scopes)
    elif match_keyword(keyword, "kaar"):
        create_sub(line_body, block, variables)
    elif match_keyword(keyword, "yotastam"):
        while_loop(line_body, block, scopes)
    elif match_keyword(keyword, "agr"):
        if_statement(line_body, block, bid, scopes)
    elif match_keyword(keyword, "agrn:"):
        else_statement(line_body, block, bid, scopes)
    elif match_keyword(keyword, "tele-agr"):
        elseif_statement(line_body, block, bid, scopes)
    elif match_keyword(keyword, "faetrow"):
        break_loop = True
    elif match_keyword(keyword, "pak-broh"):
        continue_loop = True
    elif match_keyword(keyword, "di"):
        return_value_switch = True
        return_value = expr.collapse(call_function, line_body, *scopes) if line_body != None else types.NONE()
    else:
        line_body = "" if line_body == None else line_body
        expr.collapse(call_function, keyword + " " + line_body, *scopes)

def __get_next_bid():
    global block_id
    block_id += 1
    return block_id

def execute_parsed_block(parsed_block, scopes):
    block_id = __get_next_bid()
    conditionals_info[block_id] = {
        "was_last_conditional" : False,
        "last_condition_status": False
    }
    scopes = [scopes[0]] if len(scopes) == 2 else []
    for instruction in parsed_block:
        execute(*instruction, bid = block_id, scopes = scopes)
        if break_loop or continue_loop or return_value_switch: break
    del conditionals_info[block_id]
    
def execute_block(block, scopes = []):
    parsed_block = parsecode.parse_block(block)
    execute_parsed_block(parsed_block, scopes)

def call_function(function, *arguments):
    global return_value_switch
    parsed_block = parsecode.parse_block(function.body)
    block_id = __get_next_bid()
    conditionals_info[block_id] = {
        "was_last_conditional" : False,
        "last_condition_status": False
    }
    scope = {}
    i = 0
    for arg in function.arguments:
        scope[arg.strip()] = arguments[i] if i < len(arguments) else types.NONE()
        i += 1
    for instruction in parsed_block:
        execute(*instruction, bid = block_id, scopes = [scope])
        if return_value_switch:
            return_value_switch = False
            return return_value
    return types.NONE()