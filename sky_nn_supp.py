'''
SkyNN supporting class
'''

# Chris' snek 
from colorama import init
init()

Fore_RED = '\033[31m'
Fore_BLUE = '\033[34m'
Fore_GREEN = '\033[32m'
Fore_YELLOW = '\033[33m'
Fore_MAGENTA = '\033[35m'
Fore_CYAN = '\033[36m'
Fore_WHITE = '\033[37m'

forecolors = [Fore_RED, Fore_BLUE, Fore_GREEN, Fore_YELLOW, Fore_MAGENTA, Fore_CYAN, Fore_WHITE]


# https://gist.github.com/garrettdreyfus/8153571
def yes_or_no(question):
    reply = str(input(question+' (y/n): ')).lower().strip()
    if reply[0] == 'y':
        return True
    if reply[0] == 'n':
        return False
    else:
        return yes_or_no("Uhhhh... please enter ")
        
        
def green(str):
    return(Fore_GREEN + str + Fore_WHITE)

def red(str):
    return(Fore_RED + str + Fore_WHITE)

def yellow(str):
    return(Fore_YELLOW + str + Fore_WHITE)
    
def cyan(str):
    return(Fore_CYAN + str + Fore_WHITE)