# Select everything from the first "$1" and after it
# \$1.*

# Select lines that only contain one word with no digits
# ^\s*[A-Za-z]+\s*$

# If string has 2 or more numbers together
# \d{2,}

# Select lines with special characters, but likely just replace these with blank space
# .*[!@#$%^&*()+,.?":{}|<>].*

# If string has 3 or more of any character in a row
# (.)\1\1

# Fine all duplicate phrases that repeat one after another
# \b(\w+(?:\s*\w*))\s+\1\b
# \b(\w+)\b(?=.*\b\1)

# Find things after a slash
# /\b(\w+)\s

# ^(?=.*web[^s\s\d][^\w]).*$
# web(?=[\s\d\W[a-rt-zA-RT-Z]])
# Regex: (web)([^a-rt-zA-RT-Z\s]?)+(cam)([^a-rt-zA-RT-Z\s]?)
# Regex: (web)([^a-rt-zA-RT-Z]?)([\s\d\W])
# Regex: (web|cam)([^a-rt-zA-RT-Z]?)([\s\d\W]{1,})
# Regex: (?=.*web([^a-rt-zA-RT-Z]?)([\s\d\W]{1,})
# Regex: ^(?=.*(web)([^a-rt-zA-RT-Z]?)([\s\d\W]{1,}))(?=.*(cam)([^a-rt-zA-RT-Z]?)([\s\d\W]{1,})).*$
# Regex: ^(?=.*((web,cam) ([^a-rt-zA-RT-Z]?) ([\s\d\W]{1,}) ) ).*$
# RegexSimpleCurrent: ^(?=.*web)(?=.*cam).*$
# true if string contains "web" and "cam" in it, except when immediate letters follow "web" or "cam"
# True Examples...
# web cam
# webs cam
# web cams
# webs cams
# web.cam
# web-cam
# web+cam
# web?cam
# web=cam
# web1cam
# webs1cams
# webs cama
# web-cama
# web?cama
# web1cama
# web a cam
# web  a cam
# False Examples...
# webcam
# webacam
# weba cam
# weba cams
# weba cama
# weba.cam
# weba+cam
# weba=cam
# weba1cam
