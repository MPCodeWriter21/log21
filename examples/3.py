import json

import log21

data = json.load(open('json.json', 'r'))

# Prints data using python's built-in print function
print(data)

# Uses `log21.pprint` to print the data
log21.pprint(data)

# Uses `log21.tree_print` to print the data
log21.tree_print(data)
