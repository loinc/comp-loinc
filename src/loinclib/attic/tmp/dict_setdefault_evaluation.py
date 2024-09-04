
d = {'A': 'a'}

def evaluated():
  print('evaluated')

print('get A')
d.get('A')

print('get A, default')
d.get('A', evaluated())
