# log21.Colors.py
# CodeWriter21

import re as _re
from typing import Union as _Union, Sequence as _Sequence

import webcolors as _webcolors

__all__ = [
    'Colors', 'get_color', 'get_colors', 'ansi_escape', 'get_color_name',
    'closest_color', 'hex_escape', 'RESET', 'BLACK', 'RED', 'GREEN', 'YELLOW',
    'BLUE', 'MAGENTA', 'CYAN', 'WHITE', 'BACK_BLACK', 'BACK_RED', 'BACK_GREEN',
    'BACK_YELLOW', 'BACK_BLUE', 'BACK_MAGENTA', 'BACK_CYAN', 'BACK_WHITE',
    'GREY', 'LIGHT_RED', 'LIGHT_GREEN', 'LIGHT_YELLOW', 'LIGHT_BLUE',
    'LIGHT_MAGENTA', 'LIGHT_CYAN', 'LIGHT_WHITE', 'BACK_GREY', 'BACK_LIGHT_RED',
    'BACK_LIGHT_GREEN', 'BACK_LIGHT_YELLOW', 'BACK_LIGHT_BLUE',
    'BACK_LIGHT_MAGENTA', 'BACK_LIGHT_CYAN', 'BACK_LIGHT_WHITE'
]

# Regex pattern to find ansi colors in message
ansi_escape = _re.compile(r'\x1b\[((?:\d+)(?:;(?:\d+))*)m')
hex_escape = _re.compile(r'\x1b(#[0-9a-fA-F]{6})h([f|b])')

RESET = '\033[0m'
BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[37m'
BACK_BLACK = '\033[40m'
BACK_RED = '\033[41m'
BACK_GREEN = '\033[42m'
BACK_YELLOW = '\033[43m'
BACK_BLUE = '\033[44m'
BACK_MAGENTA = '\033[45m'
BACK_CYAN = '\033[46m'
BACK_WHITE = '\033[47m'
GREY = '\033[90m'
LIGHT_RED = '\033[91m'
LIGHT_GREEN = '\033[92m'
LIGHT_YELLOW = '\033[93m'
LIGHT_BLUE = '\033[94m'
LIGHT_MAGENTA = '\033[95m'
LIGHT_CYAN = '\033[96m'
LIGHT_WHITE = '\033[97m'
BACK_GREY = '\033[100m'
BACK_LIGHT_RED = '\033[101m'
BACK_LIGHT_GREEN = '\033[102m'
BACK_LIGHT_YELLOW = '\033[103m'
BACK_LIGHT_BLUE = '\033[104m'
BACK_LIGHT_MAGENTA = '\033[105m'
BACK_LIGHT_CYAN = '\033[106m'
BACK_LIGHT_WHITE = '\033[107m'


class Colors:
    """A class containing color-maps."""
    color_map = {
        'Reset': RESET,
        'Black': BLACK,
        'Red': RED,
        'Green': GREEN,
        'Yellow': YELLOW,
        'Blue': BLUE,
        'Magenta': MAGENTA,
        'Cyan': CYAN,
        'White': WHITE,
        'BackBlack': BACK_BLACK,
        'BackRed': BACK_RED,
        'BackGreen': BACK_GREEN,
        'BackYellow': BACK_YELLOW,
        'BackBlue': BACK_BLUE,
        'BackMagenta': BACK_MAGENTA,
        'BackCyan': BACK_CYAN,
        'BackWhite': BACK_WHITE,
        'Grey': GREY,
        'LightRed': LIGHT_RED,
        'LightGreen': LIGHT_GREEN,
        'LightYellow': LIGHT_YELLOW,
        'LightBlue': LIGHT_BLUE,
        'LightMagenta': LIGHT_MAGENTA,
        'LightCyan': LIGHT_CYAN,
        'LightWhite': LIGHT_WHITE,
        'BackGrey': BACK_GREY,
        'BackLightRed': BACK_LIGHT_RED,
        'BackLightGreen': BACK_LIGHT_GREEN,
        'BackLightYellow': BACK_LIGHT_YELLOW,
        'BackLightBlue': BACK_LIGHT_BLUE,
        'BackLightMagenta': BACK_LIGHT_MAGENTA,
        'BackLightCyan': BACK_LIGHT_CYAN,
        'BackLightWhite': BACK_LIGHT_WHITE,
    }
    color_map_ = {
        'reset': RESET,
        'black': BLACK,
        'red': RED,
        'green': GREEN,
        'yellow': YELLOW,
        'blue': BLUE,
        'magenta': MAGENTA,
        'cyan': CYAN,
        'white': WHITE,
        'backblack': BACK_BLACK,
        'backred': BACK_RED,
        'backgreen': BACK_GREEN,
        'backyellow': BACK_YELLOW,
        'backblue': BACK_BLUE,
        'backmagenta': BACK_MAGENTA,
        'backcyan': BACK_CYAN,
        'backwhite': BACK_WHITE,
        'grey': GREY,
        'gray': GREY,
        'lightred': LIGHT_RED,
        'lightgreen': LIGHT_GREEN,
        'lightyellow': LIGHT_YELLOW,
        'lightblue': LIGHT_BLUE,
        'lightmagenta': LIGHT_MAGENTA,
        'lightcyan': LIGHT_CYAN,
        'lightwhite': LIGHT_WHITE,
        'backgrey': BACK_GREY,
        'backlightred': BACK_LIGHT_RED,
        'backlightgreen': BACK_LIGHT_GREEN,
        'backlightyellow': BACK_LIGHT_YELLOW,
        'backlightblue': BACK_LIGHT_BLUE,
        'backlightmagenta': BACK_LIGHT_MAGENTA,
        'backlightcyan': BACK_LIGHT_CYAN,
        'backlightwhite': BACK_LIGHT_WHITE,
        'brightblack': GREY,
        'brightred': LIGHT_RED,
        'brightgreen': LIGHT_GREEN,
        'brightyellow': LIGHT_YELLOW,
        'brightblue': LIGHT_BLUE,
        'brightmagenta': LIGHT_MAGENTA,
        'brightcyan': LIGHT_CYAN,
        'brightwhite': LIGHT_WHITE,
        'backbrightblack': BACK_GREY,
        'backbrightred': BACK_LIGHT_RED,
        'backbrightgreen': BACK_LIGHT_GREEN,
        'backbrightyellow': BACK_LIGHT_YELLOW,
        'backbrightblue': BACK_LIGHT_BLUE,
        'backbrightmagenta': BACK_LIGHT_MAGENTA,
        'backbrightcyan': BACK_LIGHT_CYAN,
        'backbrightwhite': BACK_LIGHT_WHITE,
        'rst': RESET,
        'bk': BLACK,
        'r': RED,
        'g': GREEN,
        'y': YELLOW,
        'b': BLUE,
        'm': MAGENTA,
        'c': CYAN,
        'w': WHITE,
        'bbk': BACK_BLACK,
        'br': BACK_RED,
        'bg': BACK_GREEN,
        'by': BACK_YELLOW,
        'bb': BACK_BLUE,
        'bm': BACK_MAGENTA,
        'bc': BACK_CYAN,
        'bw': BACK_WHITE,
        'gr': GREY,
        'lr': LIGHT_RED,
        'lg': LIGHT_GREEN,
        'ly': LIGHT_YELLOW,
        'lb': LIGHT_BLUE,
        'lm': LIGHT_MAGENTA,
        'lc': LIGHT_CYAN,
        'lw': LIGHT_WHITE,
        'bgr': BACK_GREY,
        'blr': BACK_LIGHT_RED,
        'blg': BACK_LIGHT_GREEN,
        'bly': BACK_LIGHT_YELLOW,
        'blb': BACK_LIGHT_BLUE,
        'blm': BACK_LIGHT_MAGENTA,
        'blc': BACK_LIGHT_CYAN,
        'blw': BACK_LIGHT_WHITE,
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
        r_d = (r_c - requested_color[0])**2
        g_d = (g_c - requested_color[1])**2
        b_d = (b_c - requested_color[2])**2
        min_colors[(r_d + g_d + b_d)] = name
    return min_colors[min(min_colors.keys())]


def get_color_name(
    color: _Union[str, _Sequence[int], _webcolors.IntegerRGB,
                  _webcolors.HTML5SimpleColor],
    raise_exceptions: bool = False
) -> str:
    """
    Takes a color in RGB format and returns a color name close to the RGB value.

    >>>
    >>> get_color_name('#00FF00')
    'LightGreen'
    >>>
    >>> get_color_name((128, 0, 128))
    'Magenta'
    >>>

    :param color: Union[str, Sequence[int]: The input color. Example: '#00FF00',
        (128, 0, 128)
    :param raise_exceptions: bool = False: Returns empty string when raise_exceptions is
        False and an error occurs.
    :raises TypeError
    :return: str: The color name.
    """
    # Makes sure that the input parameters has valid values.
    if not isinstance(color,
                      (str, tuple, _webcolors.IntegerRGB, _webcolors.HTML5SimpleColor)):
        if raise_exceptions:
            raise TypeError(
                'Input color must be a str or Tuple[int, int, int] or '
                'webcolors.IntegerRGB or webcolors.HTML5SimpleColor'
            )
        return ''
    if isinstance(color, str):
        if color.startswith('#') and len(color) == 7:
            color = _webcolors.hex_to_rgb(color)
        elif color.isdigit() and len(color) == 9:
            color = (int(color[:3]), int(color[3:6]), int(color[6:9]))
        else:
            if raise_exceptions:
                raise TypeError('String color format must be `#0021ff` or `000033255`!')
            return ''
    if isinstance(color, _Sequence):
        if len(color) == 3:
            if not (isinstance(color[0], int) and isinstance(color[1], int)
                    and isinstance(color[2], int)):
                if raise_exceptions:
                    raise TypeError('Color sequence format must be (int, int, int)!')
                return ''
        else:
            if raise_exceptions:
                raise TypeError('Color sequence format must be (int, int, int)!')
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
    """Gets a color name and returns it in ansi format

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
        return ''
    if isinstance(color, _Sequence) and not isinstance(color, str):
        color = get_color_name(color)
        return get_color(color)

    color = color.lower()
    color = color.replace(' ', '').replace('_', '').replace('-', '')
    color = color.replace('foreground', '').replace('fore', '').replace('ground', '')
    if (color.startswith('#') and len(color) == 7) or (color.isdigit()
                                                       and len(color) == 9):
        color = get_color_name(color)
        return get_color(color)
    if color in Colors.color_map_:
        return Colors.color_map_[color]
    if ansi_escape.match(color):
        return ansi_escape.match(color).group()
    if color in Colors.change_map:
        return get_color(Colors.change_map[color])
    if raise_exceptions:
        raise KeyError(f'`{color}` not found!')
    return ''


def get_colors(*colors: str, raise_exceptions: bool = False) -> str:
    """Gets a list of colors and combines them into one.

    >>>
    >>> get_colors('LightCyan')
    '\x1b[96m'
    >>>
    >>> import log21
    >>> log21.get_logger().info(log21.get_colors('Green', 'Background White') +
    ... 'Hello World!')
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
