class Code_Tree:
    def __init__(self, line, block = None):
        self.line = line
        self.block = block
        self.type = 'tree-node'

SYMBOLS = r"+/-*%@&"
FALLBACK_END_CHARS = SYMBOLS + "({["
FALLBACK_START_CHARS = SYMBOLS + "]})"

def split_instructions(string):
    string += "\n# end block"
    for fc in FALLBACK_START_CHARS:
        string = string.replace(f"\n{fc}", fc)
    for fc in FALLBACK_END_CHARS:
        string = string.replace(f"{fc}\n", fc)
    return string.split("\n")
        
    
def str_to_tree(string):
    lines = split_instructions(string)
    lines = [line.rstrip() for line in lines if line.strip() != '']
    storing_block = False
    result = []
    current_block = ""
    block_line = None
    i = 0
    while i < len(lines):
        line = lines[i]
        if not storing_block:
            if line[-1].lstrip().endswith(':'):
                storing_block = True
                current_block = ""
                block_line = line
                block_line_no = i
            else: result.append(Code_Tree(line))
        else:
            if(block_line_no == (i - 1)):
                current_indentation = " " * (len(line) - len(line.lstrip()))
            if line.startswith(current_indentation):
                current_block += "\n" + line[len(current_indentation):]
            else:
                result.append(Code_Tree(block_line, current_block))
                storing_block = False
                continue
        i += 1
    return result



def parse_block(block):
    block = str_to_tree(block)
    parsed_block = []
    for instruction in block:
        line = tuple(instruction.line.split(" ", 1))
        keyword = line[0]
        line_body = line[1] if len(line) == 2 else None
        parsed_block.append((keyword, line_body, instruction.block))
    return parsed_block