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

### 1.5.6

Added `log21.pprint()` function. It is similar to `pprint.pprint()` function.

[Full Changes Log](/CHANGES-LOG.md)


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
            get_colors('000255000', 'BackLightWhite') + 'Light Green with Light White Background' + get_colors(
                'reset') + '!')
# This is Cyan and this is Light Green with Light White Background!
```

![Example4](https://i.imgur.com/weVPxt3.png)

---------

```python
from log21 import ColorizingStreamHandler, Logger, ColorizingFormatter

logger1 = Logger('Logger1')
logger2 = Logger('Logger2')
streamHandler1 = ColorizingStreamHandler(handle_new_line=True)
streamHandler2 = ColorizingStreamHandler(handle_new_line=False)
formatter = ColorizingFormatter('[{levelname}] {message}', style='{')
streamHandler1.setFormatter(formatter)
streamHandler2.setFormatter(formatter)
logger1.addHandler(streamHandler1)
logger2.addHandler(streamHandler2)

logger1.info('\n\n1: Hello World!')
# 
# 
# [INFO] 1: Hello World!
logger2.info('\n\n2: Hello World!')
# [INFO] 
# 
# 2: Hello World!
# 
```

![Example5](https://i.imgur.com/2Z1KHQl.png)

```python
>>>
>>> import log21
>>>
>>> l = log21.get_logger()
>>> l.warning('Pretty basic, huh?')
[14:49:41] [WARNING] Pretty basic, huh?
>>> l.critical('CONTINUE READING!! please...')
[14:50:08] [CRITICAL] CONTINUE READING!! please...
>>>
>>> my_logger = log21.get_logger(name='CodeWriter21', level=log21.INFO, fmt='{asctime} -> [{levelname}]: {message}',
... style='{', override=True)
>>>
>>> my_logger.info('FYI: My name is Mehrad.')
14:56:12 -> [INFO]: FYI: My name is Mehrad.
>>> my_logger.error(log21.get_color('LightRed') + 'Oh no! Something went wrong D:')
14:56:29 -> [ERROR]: Oh no! Something went wrong D:
>>>
>>> my_logger.debug(1 ,2 ,3)
>>> # It prints Nothing because our logger level is INFO and DEBUG level is less than INFO.
>>> # So let's modify the my_logger's level
>>> my_logger.setLevel(log21.DEBUG)
>>> # Now we try again...
>>> my_logger.debug(1, 2, 3)
14:57:34 -> [DEBUG]: 1 2 3
>>> # Well Done. Right?
>>> # Let's see more
>>> my_logger.debug('I like %s number!', args=('21', ), end='\033[0m\n\n\n')
15:01:43 -> [DEBUG]: I like 21 number!


>>> # Well, I've got a question...
>>> # Do you know the name of this color?
>>> # #888888
>>> # Oh ya! I can use get_color_name
>>> log21.get_color_name('#888888')
'gray'
>>> # Oh thank you dear!
>>> # Yes I knew that was grey -_- But I wanted to introduce my little friend ☺
>>> # See you soon!
>>>
```

About
-----
Author: CodeWriter21 (Mehrad Pooryoussof)

GitHub: [MPCodeWriter21](https://github.com/MPCodeWriter21)

Telegram Channel: [@CodeWriter21](https://t.me/CodeWriter21)

Aparat Channel: [CodeWriter21](https://www.aparat.com/CodeWriter21)