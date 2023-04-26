import getfile
import execute
from os import path
from sys import argv

filename = None


if not filename:
    try:
        filename = argv[1:][0]
        outfilename = argv[1:][1] if len(argv) > 2 else None
    except IndexError:
        print("fatal : filename was not provided.")
        exit()
if not path.exists(filename):
    print(f"fatal : no file was found with the path >{filename}<.")
    exit()


getfile.read_file(filename)
file_content = getfile.last_buffer

execute.execute_block(file_content)
