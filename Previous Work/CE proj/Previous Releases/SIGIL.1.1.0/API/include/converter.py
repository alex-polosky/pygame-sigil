for x in '''
'''.split('\n'):
	print "document.write('" + x.replace("'", "\\'") + "\\n');"