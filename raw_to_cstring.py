#!/usr/local/bin/python


import pyperclip

paste = pyperclip.paste()
s = list(paste)
dest = list('"\\x')
'''for i in s:
	if (i != " "):
		dest.append(i)
	else:
		dest.append('","\\x')
dest.append('"')
print "".join(dest)

'''

for i in s:
	if (i != " "):
		dest.append(i)
	else:
		dest.append('\\x')
dest.append('"')
print "".join(dest)


