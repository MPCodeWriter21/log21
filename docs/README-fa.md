log21
=====

![version](https://img.shields.io/pypi/v/log21)
![stars](https://img.shields.io/github/stars/MPCodeWriter21/log21)
![forks](https://img.shields.io/github/forks/MPCodeWriter21/log21)
![repo size](https://img.shields.io/github/repo-size/MPCodeWriter21/log21)
[![CodeFactor](https://www.codefactor.io/repository/github/mpcodewriter21/log21/badge)](https://www.codefactor.io/repository/github/mpcodewriter21/log21)

<div style="direction: rtl">
log21 یک پکیج ساده پایتون است که به شما کمک می کند مطالب مختلف را به صورت رنگی در کنسول ویندوز یا سیستم عامل های دیگر به
سادگی چاپ کنید.
</div>

<div style="direction: rtl">
<h2>امکانات</h2>

+ متن های رنگی : هدف اصلی این پکیج پایتون در ابتدا نوشتن متون رنگی با پشتیبانی از کد رنگ های ANSI در محیط خط فرمان
  ویندوز بود.
+ تجزیه و تحلیل ورودی های خط فرمان : این پکیج دارای یک کلاس به نام ColorizingArgumentParser است که قابل استفاده به صورت
  مشابه argparse.ArgumentParser می باشد با این تفاوت که این کلاس خروجی های رنگی چاپ می کند.
+ Logging : پکیج log21 قابلیت های ماژول logging را به صورت رنگی و با امکانات بیشتر مانند تغییر levelname ارائه می دهد.
+ چاپ زیبا : آیا تا به حال خواسته اید خروجی ماژول pprint را رنگی کنید؟ log21 این کار را برایتان انجام می دهد!
+ چاپ درختی : شما می توانید یک دیکشنری با لیست را به تابع log21.tree_print ورودی دهید و تابع آن را به صورت درخت مانند
  پرینت خواهد کرد. به علاوه خروجی رنگی خواهد بود!
+ نوار پیشرفت(ProgressBar) : نوار پیشرفت log21 را می توان برای نشان دادن پیشرفت یک فرآیند به روشی زیبا استفاده کرد.
+ پنجره لاگینگ(LoggingWindow) : به شما کمک می کند تا پیام ها را چاپ و کد خود را در پنجره ای غیر از خط فرمان اشکال زدایی
  کنید.
+ ایده ای دارید؟ به راحتی می توانید [یک مساله طرح کنید](https://github.com/MPCodeWriter21/log21/issues) یا یک pull
  request ارسال کنید.

</div>

![مسائل](https://img.shields.io/github/issues/MPCodeWriter21/log21)
![مشارکت کنندگان](https://img.shields.io/github/contributors/MPCodeWriter21/log21)

<div style="direction: rtl">
<h2>نصب و راه اندازی</h2>

خب، log21 یک پکیج پایتون است، بنابراین اولین چیزی که نیاز دارید پایتون است.

اگر پایتون را نصب نکرده‌اید، لطفاً از [Python.org](https://python.org) دیدن کنید و آخرین نسخه پایتون را نصب کنید.

سپس می توانید log21 را با استفاده از ماژول pip نصب کنید:

```shell
python -m pip install log21 -U
```

یا می توانید این مخزن(repository) را کلون کرده و کد زیر را اجرا کنید:

```shell
python setup.py install
```

</div>


<h2 style="direction: rtl">مثال های استفاده:</h2>

```python3
import log21

log21.print(log21.get_color('#FF0000') + 'This' + log21.get_color((0, 255, 0)) + ' is' + log21.get_color('Blue') +
            ' Blue' + log21.get_colors('BackgroundWhite', 'Black') + ' 8)')

logger = log21.get_logger('My Logger', level_names={21: 'SpecialInfo', log21.WARNING: ' ! ', log21.ERROR: '!!!'})
logger.info('You are reading the README.md file...')

logger.log(21, 'Here', '%s', 'GO!', args=('we',))

logger.setLevel(log21.WARNING)
logger.warning("We can't log messages with a level less than 30 anymore!")

logger.debug("You won't see this!")
logger.info("Am I visible?")

logger.error(log21.get_colors('LightRed') + "I'm still here ;1")
```

![Basic Logging](https://github.com/MPCodeWriter21/log21/raw/master/screen-shots/example-1.png)

----------------

```python3
import log21
from log21 import ColorizingArgumentParser, get_logger, get_colors as gc

parser = ColorizingArgumentParser(description="This is a simple example of a ColorizingArgumentParser.",
                                  colors={'help': 'LightCyan'})
parser.add_argument('test1', action='store', help='Test 1')
parser.add_argument('test2', action='store', help='Test 2')
parser.add_argument('--optional-arg', '-o', action='store', type=int, help='An optional integer')
parser.add_argument('--verbose', '-v', action='store_true', help='Increase verbosity.')

args = parser.parse_args()

logger = get_logger('My Logger', level_names={log21.DEBUG: ' ? ', log21.INFO: ' + ', log21.WARNING: ' ! ',
                                              log21.ERROR: '!!!'})

if args.verbose:
    logger.setLevel(log21.DEBUG)
else:
    logger.setLevel(log21.INFO)

logger.debug(gc('LightBlue') + 'Verbose mode on!')

logger.debug('Arguments:\n'
             '\tTest 1: %s\n'
             '\tTest 2: %s\n'
             '\tOptional: %s', args=(args.test1, args.test2, args.optional_arg))

logger.info(gc('LightGreen') + args.test1)

logger.info(gc('LightWhite') + 'Done!')

```

![No argument](https://github.com/MPCodeWriter21/log21/raw/master/screen-shots/example-2.1.png)

![Help](https://github.com/MPCodeWriter21/log21/raw/master/screen-shots/example-2.2.png)

![Valid example 1](https://github.com/MPCodeWriter21/log21/raw/master/screen-shots/example-2.3.png)

![Valid example 2](https://github.com/MPCodeWriter21/log21/raw/master/screen-shots/example-2.4.png)

![Valid example 3](https://github.com/MPCodeWriter21/log21/raw/master/screen-shots/example-2.5.png)

------------------

```python3
import json
import log21

data = json.load(open('json.json', 'r'))

# Prints data using python's built-in print function
print(data)

# Uses `log21.pprint` to print the data
log21.pprint(data)

# Uses `log21.tree_print` to print the data
log21.tree_print(data)
```

![Python print](https://github.com/MPCodeWriter21/log21/raw/master/screen-shots/example-3.1.png)
![log21 pretty print](https://github.com/MPCodeWriter21/log21/raw/master/screen-shots/example-3.2.png)
![log21 tree print 1](https://github.com/MPCodeWriter21/log21/raw/master/screen-shots/example-3.3.1.png)
![log21 tree print 1](https://github.com/MPCodeWriter21/log21/raw/master/screen-shots/example-3.3.2.png)

------------------

```python3
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
window.info('\033#0000FFhf\033[103mThis is message with BLUE foreground and YELLOW background.')

import random, string

# And here is a text with random colors
text = 'I have random colors XD'
colored_text = ''
for character in text:
    color = '\033#' + ''.join(random.choice(string.hexdigits) for _ in range(6)) + 'hf'
    colored_text += color + character

window.error(colored_text)

# See more examples in 
# https://github.com/MPCodeWriter21/log21/blob/066efc1e72542531012d36974bbf6cd4c5941378/log21/LoggingWindow.py#L155
# and
# https://github.com/MPCodeWriter21/log21/blob/066efc1e72542531012d36974bbf6cd4c5941378/log21/__init__.py#L144

```

![The LoggingWindow](https://github.com/MPCodeWriter21/log21/raw/master/screen-shots/example-4.png)

------------------

```python3
# Example 1
import log21, time

# Define a very simple log21 progress bar
progress_bar = log21.ProgressBar()

# And here is a simple loop that will print the progress bar
for i in range(100):
    progress_bar(i + 1, 100)
    time.sleep(0.08)

# Example 2
import time, random
from log21 import ProgressBar, get_colors as gc

# Let's customize the progress bar a little bit this time
progress_bar = ProgressBar(
    width=50,
    fill='#',
    empty='-',
    prefix='[',
    suffix=']',
    colors={'progress in-progress': gc('Bright Red'), 'progress complete': gc('Bright Cyan'),
            'percentage in-progress': gc('Green'), 'percentage complete': gc('Bright Cyan'),
            'prefix-color in-progress': gc('Bright White'), 'prefix-color complete': gc('Bright White'),
            'prefix-color failed': gc('Bright White'), 'suffix-color in-progress': gc('Bright White'),
            'suffix-color complete': gc('Bright White'), 'suffix-color failed': gc('Bright White')})

for i in range(84):
    progress_bar(i + 1, 84)
    time.sleep(random.uniform(0.05, 0.21))

```

![ProgressBar - Example 1](https://github.com/MPCodeWriter21/log21/raw/master/screen-shots/example-5.1.gif)
![ProgressBar - Example 2](https://github.com/MPCodeWriter21/log21/raw/master/screen-shots/example-5.2.gif)

<div style="direction: rtl">
درباره
-----
نویسنده: کدنویس۲۱ (مهراد پوریوسف)

گیت هاب: [MPCodeWriter21](https://github.com/MPCodeWriter21)

کانال تلگرام: [@CodeWriter21](https://t.me/CodeWriter21)

کانال آپارات: [CodeWriter21](https://www.aparat.com/CodeWriter21)

### مجوز

![لایسنس](https://img.shields.io/github/license/MPCodeWriter21/log21)

[apache-2.0](http://www.apache.org/licenses/LICENSE-2.0)

### اهدا کیند

:به منظور حمایت از این پروژه، می توانید مقداری کریپتو به انتخاب خود اهدا کنید

[آدرس های رمزارز](https://github.com/MPCodeWriter21/log21/blob/master/DONATE.md)

یا اگر نمی توانید، به [این پروژه](https://github.com/MPCodeWriter21/log21) در GitHub ستاره بدهید :)


ارجاع ها
----------

+ کد های رنگ ANSI (
  ویکیپدیا): [https://en.wikipedia.org/wiki/ANSI_escape_code](https://en.wikipedia.org/wiki/ANSI_escape_code#Colors)

</div>
