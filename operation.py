import usf_types as types
def ADD(l,r):
    if type(l.data) == str:
      return types.STRING(l.data + str(r.data))
    else:
      added = l.data + r.data
      if type(added) == float:
          return types.FLOAT(added)
      else:
          return types.INTEGER(added)

def SUB(l,r):
    subbed = l.data - r.data
    if type(subbed) == float:
        return types.FLOAT(subbed)
    else:
        return types.INTEGER(subbed)

def MUL(l,r):
    dived = l.data * r.data
    if type(dived) == float:
        return types.FLOAT(dived)
    else:
        return types.INTEGER(dived)

def DIV(l,r):
    return types.FLOAT(l.data / r.data)

def POW(l,r):
    return types.FLOAT(l.data ** r.data)

def FLOOR_DIV(l,r):
    return types.INTEGER(l.data // r.data)

def MOD(l,r):
    modded = l.data % r.data
    if type(modded) == float:
        return types.FLOAT(modded)
    else:
        return types.INTEGER(modded)

def AND(l,r):
    return types.BOOL(l.data and r.data)

def OR(l,r):
    return types.BOOL(l.data or r.data)

def IN(l,r):
    for d in r.data:
        if l.data == d.data: return types.BOOL(True)
    return types.BOOL(False)

def EQUALS(l,r):
    return types.BOOL(l.data == r.data)

def LGT(l,r):
    return types.BOOL(l.data > r.data)

def LLT(l,r):
    return types.BOOL(l.data < r.data)

def NOT_EQUALS(l,r):
    return types.BOOL(l.data != r.data)

def NOT(a):
    return types.BOOL(not a.data)