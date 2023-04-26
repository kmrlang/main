last_buffer = None
def read_file(filename):
    global last_buffer 
    f = open(filename)
    data = f.read()
    f.close()
    last_buffer = data
    return data
