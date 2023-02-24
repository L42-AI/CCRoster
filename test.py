import re

string = "1200"
if re.match("^(?!2[4-9])(([01][0-9])|(2[0-3]))(?!6)[0-5][0-9]$", string):
    print("String matches the pattern.")
else:
    print("String does not match the pattern.")