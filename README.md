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

Examples:
---------

```python
from log21 import get_logger

logger = get_logger()

logger.warning('\x1b[91mBe careful!')
# [21:21:21] [warning] Be careful!
```

![Example1](https://i.imgur.com/oDb6G6U.png)

---------

```python
import log21

logger = log21.get_logger(name='Logger21', level=log21.DEBUG, show_level=False)

logger.debug('\u001b[34mHere we are!')
# [21:21:21] Here we are!
```

![Example2](https://i.imgur.com/frIW7RJ.png)

---------

```python
from log21 import ColorizingStreamHandler, Logger, ERROR

logger = Logger('MyLogger')
streamHandler = ColorizingStreamHandler()
logger.addHandler(streamHandler)

logger.log(ERROR, '%sAn', '%serror', '%soccurred!', args=('\033[31m', '\033[91m', '\033[31m'))
# An error occurred!
```

![Example3](https://i.imgur.com/BGdZyY2.png)

About
-----
Author: CodeWriter21 (Mehrad Pooryoussof)

GitHub: [MPCodeWriter21](https://github.com/MPCodeWriter21)

Telegram Channel: [@CodeWriter21](https://t.me/CodeWriter21)

Aparat Channel: [CodeWriter21](https://www.aparat.com/CodeWriter21)