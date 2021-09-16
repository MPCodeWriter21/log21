log21
=====

A simple logging package that helps you log colorized messages in Windows console and other operating systems.


Install
-------

To install log21 you can simply use the `pip install log21` command:

```commandline
python -m pip install log21
```

Or you can clone [the repository](https://github.com/MPCodeWriter21/log21) and run:

```commandline
python setup.py install
```

Changes
-------

### 1.4.4

`get_color` function now supports hexadecimal and decimal RGB values.

Examples:
---------

```python
from log21 import get_logger, get_colors

logger = get_logger()

logger.warning(get_colors('light red', 'background-white'), 'careful!')
# [21:21:21] [warning] careful!
```

![Example1](https://i.imgur.com/TM6DK0e.png)

---------

```python
import log21

logger = log21.get_logger(name='Logger21', level=log21.DEBUG, show_level=False)

logger.debug(log21.get_color('blue') + 'Here we are!')
# [21:21:21] Here we are!
```

![Example2](https://i.imgur.com/45fFs7F.png)

---------

```python
from log21 import ColorizingStreamHandler, Logger, ERROR

logger = Logger('MyLogger')
streamHandler = ColorizingStreamHandler()
logger.addHandler(streamHandler)

logger.log(ERROR, '%sAn', '%serror', '%soccurred!', args=('\u001b[31m', '\x1b[91m', '\033[31m'))
# An error occurred!
```

![Example3](https://i.imgur.com/S06PPKx.png)

---------

```python
from log21 import get_logger, get_colors

logger = get_logger("LOG21", show_time=False)

logger.info('This is', get_colors('#008888') + 'Cyan', get_colors('rst') + 'and this is',
            get_colors('000128000', 'BackWhite') + 'Green with White Background' + get_colors('reset') + '!')
# This is Cyan and this is Green with White Background!
logger.info('This is', get_colors('#00efef') + 'Light Cyan', get_colors('rst') + 'and this is',
            get_colors('000255000', 'BackLightWhite') + 'Light Green with Light White Background' + get_colors('reset') + '!')
# This is Cyan and this is Light Green with Light White Background!
```

![Example4](https://imgur.com/weVPxt3)

About
-----
Author: CodeWriter21 (Mehrad Pooryoussof)

GitHub: [MPCodeWriter21](https://github.com/MPCodeWriter21)

Telegram Channel: [@CodeWriter21](https://t.me/CodeWriter21)

Aparat Channel: [CodeWriter21](https://www.aparat.com/CodeWriter21)