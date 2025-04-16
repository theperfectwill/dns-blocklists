keywordsFile="keywords.txt"
errorLogFile="errorLog.txt"

singlePlainFile="singlePlain.txt"
singleNumberFile="singleNumber.txt"
hyphenFile="hyphen.txt"
numberFile="number.txt"
spaceFile="space.txt"
underscoreFile="underscore.txt"
specialFile="special.txt"

if [[ ! -f $keywordsFile ]]; then
    echo "Error: $keywordsFile does not exist." >&2
    exit 1
fi

# Excess Extractions In Order...
# Excess Word Lines Only
# Excess Character Lines Only
rg --pcre2 -e '^\s*[a-zA-Z]+\s*$' -e '^.*(.)\1{2,}.*$' "$keywordsFile" >"excess.txt" 2>$errorLogFile
# ^(?=.*\b(\w+)\s+\1\b)(?=.*(.)(\2{1,})).*$

# Excess Extractions...
sed -i '' '(?=.*[^\w\s+]).*' keywords.txt

# Excess Word Lines Only
# rg --pcre2 '(\b\w+\b).*\1.*$' "$keywordsFile" >"excess.txt" 2>$errorLogFile
# Excess Character Lines Only
# rg --pcre2 '(.)\1\1' "$keywordsFile" >"excess.txt" 2>$errorLogFile

# Extractions...

# Word Single Lines Only
rg --pcre2 -e '^\s*[a-zA-Z]+\s*$' "$keywordsFile" >"wordSingle.txt" 2>$errorLogFile
# Word Repeat Lines Only
# awk '/^[A-Za-z]+$/' "$keywordsFile" >"wordSingle.txt" 2>$errorLogFile
# Number Single Lines Only
# awk '/^[0-9]$/' "$keywordsFile" >"numberSingle.txt" 2>$errorLogFile
# Number Repeat Lines Only
# awk '/.*\d{2,}.*$/' "$keywordsFile" >"numberRepeat.txt" 2>$errorLogFile

if [[ $? -ne 0 ]]; then
    echo "Error occurred during grep. Check $errorLogFile for details." >&2
    exit 1
fi
