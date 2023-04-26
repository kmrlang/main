def identifier(identifier):
    return
    identifier = identifier.strip()
    if isalnum(identifier) or identifier.startswith(tuple("1234567890")) or identifier == "":
        print("Failure : identifier is not valid : Syntax Error")
        exit()

def isalnum(string):
    string = string.lower()
    for c in string:
        if c not in "abcdefghijklmnopqrstuvwxyz1234567890":
            return False
    return True