class STRING:
    def __init__(self, data):
        self.data = str(data)
        self.type = "str"
    
    def get(self):
        return self.data

class FLOAT:
    def __init__(self, data):
        self.data = float(data)
        self.type = "float"
    def get(self):
        return self.data
    

class INTEGER:
    def __init__(self, data):
        self.data = int(data)
        self.type = "int"
    
    def get(self):
        return self.data

class BOOL:
    def __init__(self, data):
       self.data = bool(data)
       self.type = "bool"
    def get(self):
        return self.data

class FUNCTION:
    def __init__(self, body, arguments):
        self.body = body
        self.type = 'sub'
        self.instances = {}
        self.arguments = arguments
        self.data = ""
    def get(self):
        return "sub()"

class ARRAY:
    def __init__(self, data):
        self.data = list(data)
        self.type = "array"
    def get(self):
        return self.data

class NONE:
    def __init__(self):
        self.data = None
        self.type = "none"
    def get(self):
        return "none"

class DICT:
    def __init__(self, data):
        self.data = dict(data)
        self.type = "dict"
    def get(self):
        return self.data


class BUILT_IN_SUB:
    def __init__(self, data):
        self.data = data
        self.type = "builtinsub"
    def get(self):
        return "<built-in sub>"


def auto(data):
    data_type = type(data)
    if data_type == int:
        return INTEGER(data)
    elif data_type == float:
        return FLOAT(data)
    elif data_type == str:
        return STRING(data)
    elif data_type == dict:
        return DICT(data)
    elif data_type == list:
        return ARRAY(data)
    elif data == None:
        return NONE()
    elif data_type.__name__ == 'builtin_function_or_method':
        return BUILT_IN_SUB(data)
    