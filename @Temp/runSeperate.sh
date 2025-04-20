echo
echo "Starting..."
echo

echo "Setting out variables..."
echo

# Set our variables
outputFile="output.txt"

# Run our Search Repalce Routines
# sed '/pattern/d' $outputFile
sed -i '' '/.*(sex|porn|adult|xx|xxx|xxxx|xxxxx).*/d' $outputFile
# Add our regex pattern for all dns blocking of these words
echo "/^(?=.*sex[^s\s\d][^\w]).*$/" $outputFile
echo "/^(?=.*porn[^s\s\d][^\w]).*$/" $outputFile
echo "/^(?=.*adult[^s\s\d][^\w]).*$/" $outputFile
echo "/^(?=.*xx[^s\s\d][^\w]).*$/" $outputFile
echo "/^(?=.*xxx[^s\s\d][^\w]).*$/" $outputFile
echo "/^(?=.*xxxx[^s\s\d][^\w]).*$/" $outputFile
echo "/^(?=.*xxxxx[^s\s\d][^\w]).*$/" $outputFile

# .*(fuck|screw|adult|xx|xxx|xxxx|xxxxx).*
# .*().*
.*(cfnm|caught|masturbat|colombian|couple|creampie|crempie|blouse|jamaican|ass|teacher|positions|pron|cherry|2x|3d|18|19|38|86|100|110|123|321|420|69429|adult|alert|amateur|anal|angel|ap|aunt|babe|baby|back|bang|bare|bbc|bdsm|blonde|blow|bondage|booty|boy|butt|cam|camel|casting|celeb|chat|child|clit|cock|companion|core|cosplay|cougar|crime|crotch|crumb|crush|cuckold|cum|cunt|cutie|dad|daddy|dating|dick|die|dress|eight|exploit|father|feet|female|femdom|fetish|file|fist|flag|fluid|foot|fuck|gang|gay|gender|girl|giz|gramp|grandma|grandpa|grann|grills|hard|heels|hentai|high|hole|hot|jiz|junk|latinas|lesbian|lgbtq|lilith|live|lotr|lust|male|man|material|meat|meet|milf|mischief|model|mom|mommy|mother|naked|natural|nine|nsfw|nudist|nut|orgasm|panties|panty|partner|penis|people|pleasure|princess|profanity|public|pussy|readyforentrance|redheads|screw|shave|shemales|shock|sissie|slut|sperm|squirt|stalk|step|street|teen|terror|thirst|tit|trans|tube|uncle|vagina|video|virgin|web|wild|wittol|wittold|woman|xx|xxx|xxxx|xxxxx|xyz|yoga|young).*


echo
echo "Completed!"
echo