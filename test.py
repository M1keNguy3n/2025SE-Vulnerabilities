text = '%3Ciframe src=”javascript:alert(1)”%3E%3C/iframe%3E'
to_replace = ["%3C", "%3E", "%3B"]
replacements = ["<", ">", ";"]
text = text.replace("%3C", "<")
print(text)