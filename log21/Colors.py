# Colors.py

class Colors:
    color_map = {
        'Reset': '\033[0m',
        'Black': '\033[30m',
        'Red': '\033[31m',
        'Green': '\033[32m',
        'Yellow': '\033[33m',
        'Blue': '\033[34m',
        'Magenta': '\033[35m',
        'Cyan': '\033[36m',
        'White': '\033[37m',
        'BackBlack': '\033[40m',
        'BackRed': '\033[41m',
        'BackGreen': '\033[42m',
        'BackYellow': '\033[43m',
        'BackBlue': '\033[44m',
        'BackMagenta': '\033[45m',
        'BackCyan': '\033[46m',
        'BackWhite': '\033[47m',
        'Grey': '\033[90m',
        'LightRed': '\033[91m',
        'LightGreen': '\033[92m',
        'LightYellow': '\033[93m',
        'LightBlue': '\033[94m',
        'LightMagenta': '\033[95m',
        'LightCyan': '\033[96m',
        'LightWhite': '\033[97m',
        'BackGrey': '\033[100m',
        'BackLightRed': '\033[101m',
        'BackLightGreen': '\033[102m',
        'BackLightYellow': '\033[103m',
        'BackLightBlue': '\033[104m',
        'BackLightMagenta': '\033[105m',
        'BackLightCyan': '\033[106m',
        'BackLightWhite': '\033[107m'
    }
    color_map_lower = {'reset': '\x1b[0m',
                       'black': '\x1b[30m',
                       'red': '\x1b[31m',
                       'green': '\x1b[32m',
                       'yellow': '\x1b[33m',
                       'blue': '\x1b[34m',
                       'magenta': '\x1b[35m',
                       'cyan': '\x1b[36m',
                       'white': '\x1b[37m',
                       'backblack': '\x1b[40m',
                       'backred': '\x1b[41m',
                       'backgreen': '\x1b[42m',
                       'backyellow': '\x1b[43m',
                       'backblue': '\x1b[44m',
                       'backmagenta': '\x1b[45m',
                       'backcyan': '\x1b[46m',
                       'backwhite': '\x1b[47m',
                       'grey': '\x1b[90m',
                       'lightred': '\x1b[91m',
                       'lightgreen': '\x1b[92m',
                       'lightyellow': '\x1b[93m',
                       'lightblue': '\x1b[94m',
                       'lightmagenta': '\x1b[95m',
                       'lightcyan': '\x1b[96m',
                       'lightwhite': '\x1b[97m',
                       'backgrey': '\x1b[100m',
                       'backlightred': '\x1b[101m',
                       'backlightgreen': '\x1b[102m',
                       'backlightyellow': '\x1b[103m',
                       'backlightblue': '\x1b[104m',
                       'backlightmagenta': '\x1b[105m',
                       'backlightcyan': '\x1b[106m',
                       'backlightwhite': '\x1b[107m'}


def get_color(color: str, raise_exceptions: bool = False) -> str:
    if type(color) is not str:
        if raise_exceptions:
            raise TypeError('`color` must be str!')
        else:
            return ''
    color = color.lower()
    color = color.replace(' ', '').replace('_', '').replace('-', '')
    color = color.replace('foreground', '').replace('fore', '').replace('ground', '')
    if color in Colors.color_map_lower:
        return Colors.color_map_lower[color]
    else:
        if raise_exceptions:
            raise KeyError(f'`{color}` not found!')
        else:
            return ''
