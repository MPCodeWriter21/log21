import log21

window = log21.get_logging_window('My Logging Window', width=80)
window.font = ('Courier New', 9)

# Basic logging
window.info('This is a basic logging message.')

# Using ANSI and HEX colors
# List of ANSI colors: https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
# ANSI color format: \033[<attribute>m
window.info('\033[91mThis is RED message.')
window.info('\033[102mThis is message with GREEN background.')
# HEX color format: \033#<HEX-COLOR>hf (where f represents the foreground color) and
# \033#<HEX-COLOR>hb (where b represents the background color)
window.info('\x1b#009900hbThis is a text with GREEN background.')
window.info(
    '\033#0000FFhf\033[103mThis is message with BLUE foreground and YELLOW background.'
)

import random
import string

# And here is a text with random colors
text = 'I have random colors XD'
colored_text = ''
for character in text:
    color = '\033#' + ''.join(random.choice(string.hexdigits) for _ in range(6)) + 'hf'
    colored_text += color + character

window.error(colored_text)

window.show()

# See more examples in
# https://github.com/MPCodeWriter21/log21/blob/066efc1e72542531012d36974bbf6cd4c5941378/log21/LoggingWindow.py#L155
# and
# https://github.com/MPCodeWriter21/log21/blob/066efc1e72542531012d36974bbf6cd4c5941378/log21/__init__.py#L144
