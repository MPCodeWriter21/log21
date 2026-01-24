# Example 1
import time

import log21

# Define a very simple log21 progress bar
progress_bar = log21.ProgressBar()

# And here is a simple loop that will print the progress bar
for i in range(100):
    progress_bar(i + 1, 100)
    time.sleep(0.08)

# Example 2
import time
import random

from log21 import ProgressBar, get_colors as gc

# Let's customize the progress bar a little bit this time
progress_bar = ProgressBar(
    width=50,
    fill='#',
    empty='-',
    prefix='[',
    suffix=']',
    colors={
        'progress in-progress': gc('Bright Red'),
        'progress complete': gc('Bright Cyan'),
        'percentage in-progress': gc('Green'),
        'percentage complete': gc('Bright Cyan'),
        'prefix-color in-progress': gc('Bright White'),
        'prefix-color complete': gc('Bright White'),
        'prefix-color failed': gc('Bright White'),
        'suffix-color in-progress': gc('Bright White'),
        'suffix-color complete': gc('Bright White'),
        'suffix-color failed': gc('Bright White')
    }
)

for i in range(84):
    progress_bar(i + 1, 84)
    time.sleep(random.uniform(0.05, 0.21))
