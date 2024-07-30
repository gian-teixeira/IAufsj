import re
import os


files = sorted(os.listdir('data/input'),
               key = lambda filename : int(re.search(r'\d+', filename).group()))

print(' '.join(list(files[:25])))