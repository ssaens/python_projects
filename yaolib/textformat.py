ENDC = '\033[0m'

class fgcolors:
    BLK = '\033[90m'
    RED = '\033[91m'
    GRN = '\033[92m'
    YLW = '\033[93m'
    BLU = '\033[94m'
    MAG = '\033[95m'
    CYN = '\033[96m'
    WHT = '\033[97m'

class bgcolors:
    BLK = '\033[100m'
    RED = '\033[101m'
    GRN = '\033[102m'
    YLW = '\033[103m'
    BLU = '\033[104m'
    MAG = '\033[105m'
    CYN = '\033[106m'
    WHT = '\033[107m'

class txtemphasis:
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    BLINKOFF = '\033[25m'
    REVERSE = '\033[26m'

fg_names = {  'black' : fgcolors.BLK,
        'red' : fgcolors.RED,
        'green' : fgcolors.GRN,
        'yellow' : fgcolors.YLW,
        'blue' : fgcolors.BLU,
        'magenta' : fgcolors.MAG,
        'cyan' : fgcolors.CYN,
        'white' : fgcolors.WHT,
}

bg_names = {  'black' : bgcolors.BLK,
        'red' : bgcolors.RED,
        'green' : bgcolors.GRN,
        'yellow' : bgcolors.YLW,
        'blue' : bgcolors.BLU,
        'magenta' : bgcolors.MAG,
        'cyan' : bgcolors.CYN,
        'white' : bgcolors.WHT,
}

emp_names = {   'bold' : txtemphasis.BOLD,
                'underline' : txtemphasis.UNDERLINE,
                'blink' : txtemphasis.BLINK,
                'noblink' : txtemphasis.BLINKOFF,
                'reverse' : txtemphasis.REVERSE,
}

def cprint(text, fg, bg=None):
    fg = fg_names[fg]
    if bg:
        bg = bg_names[bg][2:5]
        color = '{0};{1}m{2}{3}'.format(fg[:-1], bg, text, ENDC)
    else:
        color = '{0}{1}{2}'.format(fg, text, ENDC)
    print(color)

def bcprint(text, bg):
    print('{0}{1}{2}'.format(bg_names[bg], text, ENDC))

def eprint(text, emp):
    print('{0}{1}{2}'.format(emp_names[emp], text, ENDC))
