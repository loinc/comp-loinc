import re

if re.search(r'\d-\d$', '9-9'):
    print(f'It ends with - and a digit')
