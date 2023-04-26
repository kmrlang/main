GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RED = '\033[91m'
END = '\033[0m'

def usf_print(data):
    global GREEN, YELLOW, BLUE, RED, END
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RED = '\033[91m'
    END = '\033[0m'
    print(get_unit_string(data))

def get_unit_string(unit):
    if unit.type == "array":
        return get_array_string(unit)
    elif unit.type == "dict":
        return get_dict_string(unit)
    elif unit.type == "str":
        return YELLOW + '"' + unit.get() + '"' + END
    elif unit.type == 'bool':
        return GREEN + ("Poz" if unit.data else "Apuz") + END
    elif unit.type in ["int"]:
        return BLUE + str(unit.get()) + END
    else:
        return RED + str(unit.get()) + END


def get_array_string(array):
    if array.data == []: return "[]"
    array_string = "["
    return array_string + ", ".join([get_unit_string(data) for data in array.data])[:-2] + END + "]"

def get_dict_string(obj):
    if obj.data == {}: return "{}"
    dict_string = "{"

    for key in obj.data.keys():
        data = obj.data[key]
        dict_string += GREEN + key + END + " : "
        dict_string += get_unit_string(data) + ", "
    return dict_string[:-2] + "}"

def usf_print_raw(data):
    global GREEN, YELLOW, BLUE, RED, END
    GREEN = ''
    YELLOW = ''
    BLUE = ''
    RED = ''
    END = ''
    print(get_unit_string(data))