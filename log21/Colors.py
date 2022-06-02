# log21.Colors.py
# CodeWriter21

import re as _re
import webcolors as _webcolors
from typing import Union as _Union, Sequence as _Sequence

__all__ = ['Colors', 'get_color', 'get_colors', 'ansi_escape', 'get_color_name', 'closest_color', 'hex_escape']

# Regex pattern to find ansi colors in message
ansi_escape = _re.compile(r'\x1b\[((?:\d+)(?:;(?:\d+))*)m')
hex_escape = _re.compile(r'\x1b(#[0-9a-fA-F]{6})h([f|b])')


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
    color_map_ = {
        'reset': '\x1b[0m',
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
        'gray': '\x1b[90m',
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
        'backlightwhite': '\x1b[107m',
        'brightblack': '\x1b[90m',
        'brightred': '\x1b[91m',
        'brightgreen': '\x1b[92m',
        'brightyellow': '\x1b[93m',
        'brightblue': '\x1b[94m',
        'brightmagenta': '\x1b[95m',
        'brightcyan': '\x1b[96m',
        'brightwhite': '\x1b[97m',
        'backbrightblack': '\x1b[100m',
        'backbrightred': '\x1b[101m',
        'backbrightgreen': '\x1b[102m',
        'backbrightyellow': '\x1b[103m',
        'backbrightblue': '\x1b[104m',
        'backbrightmagenta': '\x1b[105m',
        'backbrightcyan': '\x1b[106m',
        'backbrightwhite': '\x1b[107m',
        'rst': '\x1b[0m',
        'bk': '\x1b[30m',
        'r': '\x1b[31m',
        'g': '\x1b[32m',
        'y': '\x1b[33m',
        'b': '\x1b[34m',
        'm': '\x1b[35m',
        'c': '\x1b[36m',
        'w': '\x1b[37m',
        'bbk': '\x1b[40m',
        'br': '\x1b[41m',
        'bg': '\x1b[42m',
        'by': '\x1b[43m',
        'bb': '\x1b[44m',
        'bm': '\x1b[45m',
        'bc': '\x1b[46m',
        'bw': '\x1b[47m',
        'gr': '\x1b[90m',
        'lr': '\x1b[91m',
        'lg': '\x1b[92m',
        'ly': '\x1b[93m',
        'lb': '\x1b[94m',
        'lm': '\x1b[95m',
        'lc': '\x1b[96m',
        'lw': '\x1b[97m',
        'bgr': '\x1b[100m',
        'blr': '\x1b[101m',
        'blg': '\x1b[102m',
        'bly': '\x1b[103m',
        'blb': '\x1b[104m',
        'blm': '\x1b[105m',
        'blc': '\x1b[106m',
        'blw': '\x1b[107m',
    }
    change_map = {
        'aqua': 'LightCyan',
        'blue': 'LightBlue',
        'fuchsia': 'LightMagenta',
        'lime': 'LightGreen',
        'maroon': 'Red',
        'navy': 'Blue',
        'olive': 'Yellow',
        'purple': 'Magenta',
        'red': 'LightRed',
        'silver': 'Grey',
        'teal': 'Cyan',
        'white': 'BrightWhite',
        'yellow': 'LightYellow',
    }


def closest_color(requested_color: _Sequence[int]):
    """
    Takes a color in RGB and returns the name of the closest color to the value.
    Uses the `webcolors.CSS2_HEX_TO_NAMES` dictionary to find the closest color.

    :param requested_color: Sequence[int, int, int]: The input color in RGB.
    :return: str: The name of the closest color.
    """
    min_colors = {}
    for key, name in _webcolors.CSS2_HEX_TO_NAMES.items():
        r_c, g_c, b_c = _webcolors.hex_to_rgb(key)
        rd = (r_c - requested_color[0]) ** 2
        gd = (g_c - requested_color[1]) ** 2
        bd = (b_c - requested_color[2]) ** 2
        min_colors[(rd + gd + bd)] = name
    return min_colors[min(min_colors.keys())]


def get_color_name(color: _Union[str, _Sequence[int], _webcolors.IntegerRGB, _webcolors.HTML5SimpleColor],
                   raise_exceptions: bool = False) -> str:
    """
    Takes a color in RGB format and returns a color name close to the RGB value.

    >>>
    >>> get_color_name('#00FF00')
    'LightGreen'
    >>>
    >>> get_color_name((128, 0, 128))
    'Magenta'
    >>>

    :param color: Union[str, Sequence[int]: The input color. Example: '#00FF00', (128, 0, 128)
    :param raise_exceptions: bool = False: Returns empty string when raise_exceptions is False and an error occurs.
    :raises TypeError
    :return: str: The color name.
    """
    # Makes sure that the input parameters has valid values.
    if not isinstance(color, (str, tuple, _webcolors.IntegerRGB, _webcolors.HTML5SimpleColor)):
        if raise_exceptions:
            raise TypeError('Input color must be a str or Tuple[int, int, int] or webcolors.IntegerRGB or ' +
                            'webcolors.HTML5SimpleColor')
        else:
            return ''
    if isinstance(color, str):
        if color.startswith('#') and len(color) == 7:
            color = _webcolors.hex_to_rgb(color)
        elif color.isdigit() and len(color) == 9:
            color = (int(color[:3]), int(color[3:6]), int(color[6:9]))
        else:
            if raise_exceptions:
                raise TypeError('String color format must be `#0021ff` or `000033255`!')
            else:
                return ''
    if isinstance(color, _Sequence):
        if len(color) == 3:
            if not (isinstance(color[0], int) and isinstance(color[1], int) and isinstance(color[2], int)):
                if raise_exceptions:
                    raise TypeError('Color sequence format must be (int, int, int)!')
                else:
                    return ''
        else:
            if raise_exceptions:
                raise TypeError('Color sequence format must be (int, int, int)!')
            else:
                return ''

    # Looks for the name of the input RGB color.
    try:
        closest_name = _webcolors.rgb_to_name(tuple(color))
    except ValueError:
        closest_name = closest_color(color)
    if closest_name in Colors.change_map:
        closest_name = Colors.change_map[closest_name]
    return closest_name


def get_color(color: _Union[str, _Sequence], raise_exceptions: bool = False) -> str:
    """
    Gets a color name and returns it in ansi format
    >>>
    >>> get_color('LightRed')
    '\x1b[91m'
    >>>
    >>> import log21
    >>> log21.get_logger().info(log21.get_color('Blue') + 'Hello World!')
    [21:21:21] [INFO] Hello World!
    >>> # Note that you must run it yourself to see the colorful result ;D
    >>>

    :param color: color name(Example: Blue)
    :param raise_exceptions: bool = False:
        False: It will return '' instead of raising exceptions when an error occurs.
        True: It may raise TypeError or KeyError
    :raises TypeError: `color` must be str
    :raises KeyError: `color` not found!
    :return: str: an ansi color
    """
    if not isinstance(color, (str, _Sequence)):
        if raise_exceptions:
            raise TypeError('`color` must be str or Sequence!')
        else:
            return ''
    if isinstance(color, _Sequence) and not isinstance(color, str):
        color = get_color_name(color)
        return get_color(color)
    else:
        color = color.lower()
        color = color.replace(' ', '').replace('_', '').replace('-', '')
        color = color.replace('foreground', '').replace('fore', '').replace('ground', '')
        if (color.startswith('#') and len(color) == 7) or (color.isdigit() and len(color) == 9):
            color = get_color_name(color)
            return get_color(color)
        elif color in Colors.color_map_:
            return Colors.color_map_[color]
        elif ansi_escape.match(color):
            return ansi_escape.match(color).group()
        elif color in Colors.change_map:
            return get_color(Colors.change_map[color])
        else:
            if raise_exceptions:
                raise KeyError(f'`{color}` not found!')
            else:
                return ''


def get_colors(*colors: str, raise_exceptions: bool = False) -> str:
    """
    Gets a list of colors and combines them into one.
    >>>
    >>> get_colors('LightCyan')
    '\x1b[96m'
    >>>
    >>> import log21
    >>> log21.get_logger().info(log21.get_colors('Green', 'Background White') + 'Hello World!')
    [21:21:21] [INFO] Hello World!
    >>> # Note that you must run it yourself to see the colorful result ;D
    >>>

    :param colors: Input colors
    :param raise_exceptions: bool = False:
        False: It will return '' instead of raising exceptions when an error occurs.
        True: It may raise TypeError or KeyError
    :raises TypeError: `color` must be str
    :raises KeyError: `color` not found!
    :return: str: a combined color
    """
    output = ''
    for color in colors:
        output += get_color(str(color), raise_exceptions=raise_exceptions)
    parts = ansi_escape.split(output)
    output = '\033['
    for part in parts:
        if part:
            output += part + ';'
    if output.endswith(';'):
        output = output[:-1] + 'm'
        return output
    return ''
