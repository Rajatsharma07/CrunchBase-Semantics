import re

def latType(user_input):
#  print "Lexical Answer Type"
  m = re.search('\\b(W|w)(h|H)(O|o)\\b', user_input)
  if m is not None:
    return m.group(0).lower()

  m = re.search('\\b(W|w)(h|H)(E|e)(R|r)(E|e)\\b', user_input)
  if m is not None:
    return m.group(0).lower()

  m = re.search('\\b(W|w)(h|H)(E|e)(N|n)\\b', user_input)
  if m is not None:
    return m.group(0).lower()

  m = re.search('\\b(W|w)(h|H)(A|a)(T|t)\\b', user_input)
  if m is not None:
    return m.group(0).lower()

  m = re.search('\\b(W|w)(h|H)(Y|y)\\b', user_input)
  if m is not None:
    return m.group(0).lower()

  m = re.search('\\b(h|H)(O|o)(W|w)\\b', user_input)
  if m is not None:
    return m.group(0).lower()

  m = re.search('\\b(w|W)(h|H)(i|I)(c|C)(h|H)\\b', user_input)
  if m is not None:
    return m.group(0).lower()


