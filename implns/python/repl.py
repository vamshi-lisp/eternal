import readline

def READ(x : str) -> str:
    return x

def ENV(x : str) -> str:
    return x

def PRINT(x : str) -> str:
    return x

def REPL(x : str) -> str:
    return PRINT(ENV(READ(x)))

eof : bool = False
while (True):
    try:
        line = input("--> ")
        readline.add_history(line)
        print(REPL(line))
    except EOFError :
        eof = True
