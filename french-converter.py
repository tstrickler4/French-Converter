'''
How to Use: Mark the stressed vowel by preceding it with a "!". Mark long vowels
with a ":".

Meaning of Characters: Most characters are equivalent to their IPA values, but
for some I was too lazy to deal with unicode, so "E"="ɛ", "O"="ɔ", "J"="ʲ",
"Q"="j" (derived from "dʲ" or "gʲ", which goes through a different process than
regular "j"), "K"="k" (stemming from "qu" which resists changes associated with
regular "k"), "G"="gu" (when before a vowel, which, like "qu", resists changes
associated with regular "g"), "D"="ð", "T"="θ", "S"="ʃ", "Z"="ʒ", "L"="ʎ",
"N"="ɲ", "@"="æ", "X"="œ", "A" = "ɛ" (stemming from "aj", which resisted certain
changes associated with regular "ɛ"), and "~" means the preceding vowel is
nasalized. I may have missed some, but that should be the gist.

Caution: The vast majority of the info was pulled from the "Phonological History
of French" page on Wikipedia, but when writing the script I noticed a lot of
inconsistencies on the page, so I did my best to interpret them. Some steps are
speculated based on examples from the page, which didn't have the expected
results based on the info provided (the associated comments are marked with a
"?"). I also had to move some steps to different locations because the order
provided didn't produce the expected outcomes. There also seems to be a trend
for infinitive forms to break the rules so they normalize with the conjugated
forms, so keep that in mind. I also came across some words that just don't
follow the rules at all (I'm looking at you, "abîme"), but I guess some
irregularity is to be expected in any language. All that said, I'm sure the
script is still nowhere near perfect, so if you notice any issues, let me know.

Output: The input word will go through 6 stages: original interpretation,
Western Romance, Gallo-Ibero-Romance, Proto-French, Old French, the finally
Modern French. The actual resulting spelling will have to be interpreted from
the result because I figured the spelling would be dependent on the input
language. The output can also be adjusted slightly depending on if you allow the
first lenition to occur before or after the first vowel loss in the
Gallo-Ibero-Romance phase. In real French it was variable, but according to the
Wikipedia page, the standard was for lenition to occur before vowel loss, with
instances of the opposite being observed, so that's how I coded it. If you like
the output better the other way, you can swap the steps by setting the optional
swap parameter to True (the default is False). Note that a final /e/,
representing a schwa which stemmed from an unstressed /a/, is actually silent,
but it prevented loss of final consonants, so I left it in there even though it
technically isn't.

Anyway... Enjoy!
'''

import re

def evolve(word, swap=False):

    #prep the word (my attempts at phoneticizing the word before applying
    #changes)
    word = re.sub(r"c", "k", word)
    word = re.sub(r"x", "ks", word)
    word = re.sub(r"qu", "K", word)
    word = re.sub(r"gu(?=[aeiou!])", "G", word)
    word = re.sub(r"y", "i", word)
    word = re.sub(r"(!{0,1})i(?=[aeiou!])", r"j\1", word)
    word = re.sub(r"(?<![eiou:])(!{0,1})u(?=[aeiou!])", r"w\1", word)
    word = re.sub(r"(!{0,1})u(?=[aeiou!])", r"v\1", word)

    #print evolution of word
    print word,
    word = toWR(word)
    print word,
    word = toGIR(word, swap)
    print word,
    word = toPF(word)
    print word,
    word = toOF(word)
    print word,
    word = toMF(word)
    print word

def toWR(word):

    #?/b/, /p/ > /t/ before /t/
    word = re.sub(r"[bp]t", "tt", word)

    #introduction of short /i/ at the beginning of a word before /s/+consonant
    word = re.sub(r"^(?=s[^aeiou!])", "i", word)

    #reduction of 10 vowels to 7
    lookup = {'a':'a', 'a:':'a', 'ae':'E', 'au':'aw', 'e':'E', 'e:':'e',
            'i':'e', 'i:':'i', 'o':'O', 'o:':'o', 'oe':'e', 'u':'o', 'u:':'u'}
    word = re.sub(r"[aeiou:]{1,2}", lambda x: lookup.get(x.group(), x.group()), word)
    word = re.sub(r"(?<!!)E", "e", word)
    word = re.sub(r"(?<!!)O", "o", word)

    #loss of final /m/, ?/n/ except in monosyllables
    word = re.sub(r"([aeiouEO]{1,}[^aeiouEO!]{0,}[aeiouEO!]{1,})[mn]$", r"\1", word)
    word = re.sub(r"m$", "n", word)

    #loss of /h/ ?(i chose to leave it when initial until later based on
    #evidence which suggests that it prevents initial /j/ from becoming /dZ/ in
    #the proto-french stage)
    word = re.sub(r"(?<!^)h", "", word)

    #/ns/ > /s/
    word = re.sub(r"ns", "s", word)

    #/rs/ > /ss/ ?except when preceded by /o/
    word = re.sub(r"(?<!o)rs", "ss", word)

    #final /er/, /or/ > /re/, /ro/; ?preceding /w/ lost
    word = re.sub(r"w{0,1}([eo])r$", r"r\1", word)

    #loss of unstressed internal vowels between /k/, /g/ and /l/, /r/
    word = re.sub(r"(?<=[aeiouEO][gk])[aeiouEO](?=[lr][aeiouEO!])", "", word)

    #reduction of /e/ and /i/ in hiatus to /j/ followed by palatalization
    #(/kj/ > /kkj/ prior to palatalization)
    word = re.sub(r"[ei](?=[aeiou!])", "j", word)
    word = re.sub(r"(?<!^)kj", "kkj", word)
    word = re.sub(r"(?<![aeiouEO])j", "J", word)
    word = re.sub(r"^J", "j", word)

    #palatalization of /k/ and /g/ before front vowels
    word = re.sub(r"([kg])(?=!{0,1}[eiE])", r"\1J", word)

    #/dJ/ and /gJ/ > /j/
    word = re.sub(r"[dg]J", "Q", word)

    #end WR
    return word

def toGIR(word, swap):

    #/kJ/ and /tJ/ merge to /tsJ/
    word = re.sub(r"kkJ", "ttJ", word)
    word = re.sub(r"[tk]J", "tsJ", word)

    #/k/ > /j/ before /s/ or /t/
    word = re.sub(r"k(?=[st])", "j", word)

    #first diphthongization: /E/ > /jE/, /O/ > /wO/ in open syllables or before
    #/j/
    word = re.sub(r"!E(?=j|$|d[zZ]|t[sS]|[tdkgpb][lr]|[^aeiouEOj][aeiouEOjwJ])", "j!E", word)
    word = re.sub(r"jj", "j", word)
    word = re.sub(r"!O(?=j|$|d[zZ]|t[sS]|[tdkgpb][lr]|[^aeiouEOj][aeiouEOjwJ])", "w!O", word)

    #?/g/ > /w/ between /a/ and /o/, /u/, /w/
    word = re.sub(r"(?<=a)g(?=[ouw])", "w", word)

    #vowel loss before lenition
    if swap:

        #first unstressed vowel loss: pretonic vowels except /a/
        word = re.sub(r"([aeiouEO][^aeiouEO]{1,})[eiouEO](?=[^aeiouEO]{1,}!)", r"\1", word)

        #first lenition: voiced stops and unvoiced fricatives > voiced
        #fricatives, unvoiced stops > voiced stops, consonants before /r/ and
        #/l/ lenited, final /t/ and /d/ lenited
        lookup = {'b':'v', 'd':'D', 'g':'j', 'p':'b', 't':'d', 'k':'g', 'f':'v',
                's':'z', 'ts':'dz', 'pl':'bl', 'kl':'gl', 'gl':'jl', 'gn':'jn'}
        word = re.sub(r"(?<=[aeiouEO])[^aeiouEO!Jrwj]{1,2}(?=[aeiouEO!Jrwj])", lambda x: lookup.get(x.group(), x.group()), word)
        word = re.sub(r"(?<=[aeiouEO])d$", "D", word)
        word = re.sub(r"(?<=[aeiouEO])t$", "d", word)

        #/jn/, /nj/, /nJ/ > /N/ and /jl/, /gl/, /lJ/ > /L/
        word = re.sub(r"jn|nj|nJ", "N", word)
        word = re.sub(r"jl|gl|lJ", "L", word)

    #vowel loss after lenition
    else:

        #first lenition: voiced stops and unvoiced fricatives > voiced
        #fricatives, unvoiced stops > voiced stops, consonants before /r/ and
        #/l/ lenited, final /t/ and /d/ lenited
        lookup = {'b':'v', 'd':'D', 'g':'j', 'p':'b', 't':'d', 'k':'g', 'f':'v',
                's':'z', 'ts':'dz', 'pl':'bl', 'kl':'gl', 'gl':'jl', 'gn':'jn'}
        word = re.sub(r"(?<=[aeiouEO])[^aeiouEO!Jrwj]{1,2}(?=[aeiouEO!Jrwj])", lambda x: lookup.get(x.group(), x.group()), word)
        word = re.sub(r"(?<=[aeiouEO])d$", "D", word)
        word = re.sub(r"(?<=[aeiouEO])t$", "d", word)

        #/jn/, /nj/, /nJ/ > /N/ and /jl/, /gl/, /lJ/ > /L/
        word = re.sub(r"jn|nj|nJ|nQ", "N", word)
        word = re.sub(r"NJ", "N", word)
        word = re.sub(r"jl|gl|lJ|lQ", "L", word)
        word = re.sub(r"LJ", "L", word)

        #first unstressed vowel loss: pretonic vowels except /a/
        word = re.sub(r"([aeiouEO][^aeiouEO]{1,})[eiouEO](?=[^aeiouEO]{1,}!)", r"\1", word)

    #end GIR
    return word

def toPF(word):

    #/j/ when initial or stemming from /dJ/ or /gJ/ when preceded by a consonant
    #becomes /dZ/
    word = re.sub(r"^j|(?<![aeiouEOw])Q", "dZ", word)
    word = re.sub(r"Q", "j", word)
    word = re.sub(r"h", "", word)

    #/j/ palatalizes following consonant if present
    word = re.sub(r"(?<=j)([^aeiouEOw!])", r"\1J", word)

    #/pJ/ > /tS/, /bJ/ and /vJ/ > /dZ/, /mJ/ > /ndZ/
    word = re.sub(r"(?<=.)pJ(?=.)", "tS", word)
    word = re.sub(r"(?<=.)[bv]J(?=.)", "dZ", word)
    word = re.sub(r"(?<=.)mJ(?=.)", "ndZ", word)

    #palatized consonants eject preceding /j/ when open and a following /j/ when
    #stressed open /a/ or /e/ special cases noted below

    #/tS/ and /dZ/ eject a following /j/ but not a preceding one
    word = re.sub(r"(tS|dZ)(?=![ae]($|d[zZ]|t[sS]|[tdkgpb][lr]|[^aeiouEO][aeiouEOjw]))", r"\1j", word)

    #/ssJ/ and /dz/ eject preceding and following /j/
    #?/ts/ only ejects /following /j/ (if it were capable of ejecting preceding
    #/j/, it would be preceded by a vowel, meaning it became /dz/ during first
    #lention)
    word = re.sub(r"(ss|dz)J", r"j\1J", word)
    word = re.sub(r"(ss|dz|ts)J(?=![ae]($|d[zZ]|t[sS]|[tdkgpb][lr]|[^aeiouEO][aeiouEOjw]))", r"\1j", word)
    word = re.sub(r"(ss|dz|ts)J", r"\1", word)

    #/N/ and /L/ maintain their palatal quality at this stage

    #/rJ/ ejects a /j/, but it metathesizes when /a/ precedes
    #?(this rule doesn't seem to be super consistent, so it could go either way)
    word = re.sub(r"(!{0,1})arJ", r"j\1arJ", word)
    word = re.sub(r"(?<=[eiouEO])rJ", "jrJ", word)
    word = re.sub(r"(?<=[tdpbkg])rJ", "jrJ", word)
    word = re.sub(r"rJ(?=![ae]($|d[zZ]|t[sS]|[tdkgpb][lr]|[^aeiouEO][aeiouEOjw]))", r"rj", word)
    word = re.sub(r"rJ", "r", word)

    #all other palatals
    word = re.sub(r"(?<!^)([^j].)J", r"j\1J", word)
    word = re.sub(r"J(?=![ae]($|d[zZ]|t[sS]|[tdkgpb][lr]|[^aeiouEO][aeiouEOjw]))", r"j", word)
    word = re.sub(r"J", "", word)

    #?/o/, /jo/, /go/, /ko/ fuse with preceding /aw/ to become /Ow/
    #?(this part is a little confusing... /aw/ > /O/ has to happen after
    #palatalization of /k/ and /g/ below, but this step has to happen before the
    #second unstressed vowel loss, so i decided to temporarily use the
    #the sequence /aww/; i'm pretty sure this isn't how it actually happened,
    #but it's necessary to do it this way for the code to work properly)
    word = re.sub(r"aw[jgk]{0,1}(!{0,1})o", r"\1aww", word)
    word = re.sub(r"aw(?=[aeiouEO])", "aww", word)

    #second diphthongization: stressed open /e/ > /ej/, /o/ > /ow/, /a/ > /@/
    #when not followed by /j/
    word = re.sub(r"!e(?=$|d[zZ]|t[sS]|[tdkgpb][lr]|[^aeiouEOj][aeiouEOjw])", "!ej", word)
    word = re.sub(r"!o(?=$|d[zZ]|t[sS]|[tdkgpb][lr]|[^aeiouEOjN][aeiouEOjw])", "!ow", word)
    word = re.sub(r"!a(?!w)(?=$|d[zZ]|t[sS]|[tdkgpb][lr]|[^aeiouEOj][aeiouEOjw])", "!@", word)

    #second unstressed vowel loss: loss of unstressed vowels except /a/ (which
    #becomes schwa later) in final syllables
    #?(i moved the schwa step to after the /l/ > /w/ step in the old french
    #stage as leaving it before would prevent that step from working correctly)
    word = re.sub(r"([^aeiouEO@]{0,}[aeiouEO@][^aeiouEO@!]{0,})[eiouEO@](?=[^aeiouEO@]{0,}$)", r"\1", word)

    #second lenition: same as first
    lookup = {'b':'v', 'd':'D', 'g':'j', 'p':'b', 't':'d', 'k':'g', 'f':'v',
            's':'z', 'ts':'dz', 'pl':'bl', 'kl':'gl', 'gl':'jl', 'gn':'jn',
            'tS':'dZ'}
    word = re.sub(r"(?<=[aeiouEO@])[^aeiouEO@!Jrwj]{1,2}(?=[aeiouEO@!Jrwj])", lambda x: lookup.get(x.group(), x.group()), word)
    word = re.sub(r"(?<=[aeiouEO@])d$", "D", word)
    word = re.sub(r"(?<=[aeiouEO@])t$", "d", word)

    #?/jaj/ > /i/
    word = re.sub(r"j(!{0,1})aj", r"\1i", word)

    #/ka/ > /tSa/, /ga/ > /dZa/
    word = re.sub(r"k(?=!{0,1}[a@])", "tS", word)
    word = re.sub(r"g(?=!{0,1}[a@])", "dZ", word)

    #/@/ > /E/ (/jE/ after palatals and /aj/ before nasal when not preceded by a
    #palatal) ?(looks like it becomes /a/ before /N/)
    word = re.sub(r"(?<=[SZ])(!{0,1})@", r"j\1E", word)
    word = re.sub(r"@(?=[nm])", "aj", word)
    word = re.sub(r"@(?=N)", "a", word)
    word = re.sub(r"@", "E", word)

    #/aw/ > /O/
    word = re.sub(r"aw", "O", word)

    #geminate stops become single stops
    word = re.sub(r"([pbtdkg])\1", r"\1", word)

    #final stops and fricatives become devoiced
    lookup = {'b':'p', 'd':'t', 'g':'k', 'v':'f', 'z':'s', 'D':'T'}
    word = re.sub(r"[bdgvzD](?=[^aeiouEO]{0,}$)", lambda x: lookup.get(x.group(), x.group()), word)

    #/dz/ > /z/ except at end
    word = re.sub(r"dz(?!$)", "z", word)

    #/t/ inserted between /N/ or /L/ and /s/
    word = re.sub(r"([NL])(?=s)", r"\1t", word)

    #depalatalization of /N/ and /L/ when final, following a consonant
    #?(it looks like /N/ depalatalizes in closed syllables in general; not sure
    #if the same happens for /L/ or not because I haven't found any specific
    #examples, but i'll assume that it does until proven otherwise)
    word = re.sub(r"N(?=$|[^aeiouEOjw])", "jn", word)
    word = re.sub(r"(?<![aeiouEOjw])N", "jn", word)
    word = re.sub(r"L(?=$|[^aeiouEOjw])", "l", word)
    word = re.sub(r"(?<![aeiouEOjw])L", "l", word)

    #/jEj/ and /jej/ > /i/, /wOj/ > /uj/
    word = re.sub(r"j(!{0,1})[Ee]j", r"\1i", word)
    word = re.sub(r"w(!{0,1})Oj", r"\1uj", word)

    #end PF
    return word

def toOF(word):

    #loss of /f/, /p/, /k/ before final /s/, /t/
    word = re.sub(r"[fpk](?=[st]$)", "", word)

    #/u/ > /y/
    word = re.sub(r"u", "y", word)

    #nasalization of vowels before /n/, /m/, and ?/N/
    word = re.sub(r"(?<=[aeiouyEOjw])([nmN])", r"~\1", word)

    #?/Ej/ > /i/
    word = re.sub(r"Ej", "i", word)

    #/ej/ > /oj/ (blocked by nasalization)
    word = re.sub(r"ej(?!~)", "oj", word)

    #/ow/ > /ew/ (blocked by nasalization and labial consonants)
    word = re.sub(r"ow(?![pbm~])", "ew", word)

    #/wO/ > /wE/ ?(wikipedia says this was blocked by nasalization, but my own
    #research says otherwise)
    word = re.sub(r"w(!{0,1})O", r"w\1E", word)

    #?/wE~/ > /u~/
    word = re.sub(r"w(!{0,1})E~", r"\1u~", word)

    #lowering of /e~/ and /E~/ to /a~/ except when preceded or followed by /j/
    word = re.sub(r"(?<![j!])(!{0,1})[eE]~", r"\1a~", word)

    #loss of /D/ and /T/; resulting /a/ in hiatus reduced to schwa (/e/)
    word = re.sub(r"[DT]", "", word)
    word = re.sub(r"(?<=[aeiouyEO])a", "e", word)
    word = re.sub(r"a(?=[aeiouyEO!])", "e", word)

    #loss of /s/ before consonants
    word = re.sub(r"s(?=[^aeiouyEOjw!])", "", word)

    #final /rn/, /rm/ > /r/
    word = re.sub(r"r[nm]$", "r", word)

    #/o/ > /u/
    word = re.sub(r"o(?!j)", "u", word)
    word = re.sub(r"uw", "u", word) #?

    #/l/ > /w/ before consonants (except in the sequence /lla/
    word = re.sub(r"ll$", "w", word) #?
    word = re.sub(r"l(?!$|la|[aeiouyEOjw!])", "w", word)
    word = re.sub(r"(?<=[^jw!])(!{0,1})Ew", r"\1Eaw", word)
    word = re.sub(r"([^aeiouyEO@jw]{0,}[aeiouyEO@jw][^aeiouyEO@jw!]{0,})a(?=[^aeiouyEO@jw~]{0,}$)", r"\1e", word)

    #/ew/, /wE/ > /X/
    word = re.sub(r"ew", "X", word)
    word = re.sub(r"w(!{0,1})E(?!w)", r"\1X", word)

    #/oj/, /Oj/ > /wE/
    word = re.sub(r"(!{0,1})[oO]j", r"w\1E", word)

    #/yj/ > /yi/
    word = re.sub(r"yj", "yi", word)

    #/aj/ > /E/
    word = re.sub(r"aj", "A", word)

    #/e/ > /E/ in closed syllables
    word = re.sub(r"e(?=[^aeiouyEOXwj!~]{2,}|[^aeiouyEOXwj!~]$)", "E", word)

    #?/O/ > /o/ before /s/, /z/
    word = re.sub(r"O(?=[sz])", "o", word)

    #deaffrication: /ts/ > /s/, /tS/ > /S/, /dZ/ > /Z/
    word = re.sub(r"ts", "s", word)
    word = re.sub(r"tS", "S", word)
    word = re.sub(r"dZ", "Z", word)

    #?loss of gemination of all consonants (this must've happened at some point,
    #but it's not specified when on wikipedia)
    word = re.sub(r"([^aeiouyEOX])\1", r"\1", word)

    #end OF
    return word

def toMF(word):

    #?evolution of sequences with /w/ derived from /l/
    word = re.sub("Eaw", "o", word)
    word = re.sub(r"aw", "O", word)
    word = re.sub(r"w{0,1}(!{0,1})Ew", r"\1X", word)

    #?/Ow/ > /u/
    word = re.sub(r"[Ou]w", "u", word)

    #/ej/ > /E/
    word = re.sub(r"ej", "E", word)

    #/u~/ and /o~/ > /O~/
    word = re.sub(r"[uo]~", "O~", word)

    #denasalization of nasal vowels when the following /n/, /m/, or ?/N/ is
    #followed by a vowel
    word = re.sub(r"~(?=[nmN][aeiouyEOXjw!])", "", word)

    #deletion of /n/, /m/, and ?/N/ after remaining nasal vowels
    word = re.sub(r"~[mnN]", "~", word)

    #loss of final consonants ?(except /r/; /l/ maintained except after high
    #vowels; /k/ and /f/ also maintained after a vowel)
    word = re.sub(r"[^aeiouyEOXjwrlkKf~]$", "", word)
    word = re.sub(r"(?<=[iyu])l$", "", word)
    word = re.sub(r"(?<=[^aeiouyEOXjw])[kf]$", "", word)

    #/wE/ > /wa/ (?blocked by nasalization)
    word = re.sub(r"w(!{0,1})E(?!~)", r"w\1a", word)

    #?final /E/ > /e/ (except when stemming from /aj/) and /O/ > /o/
    word = re.sub(r"E$", "e", word)
    word = re.sub(r"O$", "o", word)
    word = re.sub(r"A", "E", word)

    #merging of /L/ with /j/
    word = re.sub(r"L", "j", word)

    #/i~/, /y~/ > /E~/
    word = re.sub(r"[iy]~", "E~", word)

    #?unstressed /a/'s in open syllables following a palatal and when final
    #become schwa (/e/)
    word = re.sub(r"(?<!^)(?<![!w])(?<=[SZ])a(?!~)(?=$|[^aeiouyEOXwj][aeiouyEOXwj!])", "e", word)

    #?loss of unstressed /e/, /E/ in hiatus
    word = re.sub(r"(?<!!)[Ee](?=[aeiouyEOXwj!])", "", word)
    word = re.sub(r"(?<=[aeiouyEOX])[Ee](?!$|~)", "", word)

    #?loss of /j/ after /S/, /Z/ when not followed by nasal vowel
    word = re.sub(r"(?<=[SZ])j(?!!{0,1}[aeiouEOX]~)", "", word)

    #end MF
    return word

#all the words from the vowel outcomes table on wikipedia
words = ["p!artem", "b!assum", "m!are", "am!a:tum", "f!agum", "b!auan",
        "mediet!a:tem", "c!a:rum", "s!eptem", "h!eri", "p!edem", "s!iccum",
        "p!e:ram", "vid!e:re", "c!e:ram", "merc!e:dem", "v!i:tam", "v!i:llam",
        "p!ortam", "s!ottum", "s!ottam", "gr!ossum", "gr!ossam", "n!ouum",
        "c!orem", "s!ubtus", "s!urdum", "n!o:dum", "d!u:rum", "n!u:llam",
        "!aurum", "c!ausam", "tr!aucon", "!annum", "c!antum", "s!a:nam",
        "!amat", "s!a:num", "f!amem", "c!anem", "d!entem", "t!enent", "b!ene",
        "t!enet", "l!ingua", "p!e:nam", "pl!e:num", "s!inum", "rac!e:mum",
        "c!i:nque", "f!i:num", "f!i:nam", "p!ontem", "b!onam", "b!onum",
        "c!omes", "d!o:num", "d!o:nat", "!u:num", "parf!u:mum", "!u:nam",
        "pl!u:mam", "f!estam", "b!e:stiam", "ab!y:ssimum", "c!ostam", "c!o:nstat",
        "f!u:stis", "f!alsum", "p!almam", "b!ellum", "b!ellam", "m!elius",
        "cap!illum", "f!iltrum", "gent!i:lem", "f!ollem", "f!ollam", "c!olpum",
        "v!olet", "p!ulsat", "c!u:lum", "aug!ustum", "p!orcum", "f!actum",
        "pal!a:tium", "pl!a:gam", "pl!acet", "p!aria", "!iacet", "c!acat",
        "oper!a:rium", "cac!a:re", "l!ectum", "s!ex", "p!eior", "t!e:ctum",
        "r!e:gem", "n!igrum", "f!e:riam", "n!octem", "h!odie", "c!oxam",
        "b!uxitam", "cr!ucem", "fr!u:ctum", "g!audia", "b!aneum", "s!anctum",
        "mont!a:neam", "p!inctum", "ins!igniam", "l!i:neam", "l!onge",
        "fr!ogna", "p!unctum", "c!uneum", "verec!undiam", "i!u:nium"]

for i in words:
    evolve(i)