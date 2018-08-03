'''
How to use: Mark the stressed vowel by preceding it with a "!". Mark long vowels
with a ":".

Meaning of characters: Most characters are equivalent to their IPA values, but
for some I was too lazy to deal with unicode, so "E"="ɛ", "O"="ɔ", "J"="ʲ",
"G"="j" (derived from "dʲ" or "gʲ", which goes through a different process than
regular "j"), "D"="ð", "T"="θ", "S"="ʃ", "Z"="ʒ", "L"="ʎ", "N"="ɲ", "@"="æ", and
"~" means the preceding vowel is nasalized. I may have missed some, but that
should be the gist.

Note: The vast majority of the info was pulled from the "Phonological History
of French" page on Wikipedia, but when writing the script I noticed a lot of
inconsistencies on the page, so I did my best to interpret them. Some steps are
speculated based on examples from the page, which didn't have the expected
results based on the info provided. All that said, I'm sure the script is still
nowhere near perfect, so if you notice any issues, let me know.

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
swap parameter to True (the default is False).

Enjoy!
'''

import re

def evolve(word, swap=False):

    #prep the word
    word = re.sub(r"c", "k", word)
    word = re.sub(r"x", "ks", word)
    word = re.sub(r"qu", "kw", word)
    word = re.sub(r"(!{0,1})i(?=[aeiou!])", r"j\1", word)
    word = re.sub(r"(!{0,1})u(?=[aeiou!])", r"w\1", word)

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

    #introduction of short /i/ at the beginning of a word before /s/+consonant
    word = re.sub(r"^(?=s[^aeiou!])", "i", word)

    #reduction of 10 vowels to 7
    lookup = {'a':'a', 'a:':'a', 'ae':'E', 'au':'aw', 'e':'E', 'e:':'e',
            'i':'e', 'i:':'i', 'o':'O', 'o:':'o', 'oe':'e', 'u':'o', 'u:':'u'}
    word = re.sub(r"[aeiou:]{1,2}", lambda x: lookup.get(x.group(), x.group()), word)
    word = re.sub(r"(?<!!)E", "e", word)
    word = re.sub(r"(?<!!)O", "o", word)

    #loss of final /m/, /n/ except in monosyllables
    word = re.sub(r"([aeiouEO]{1,}[^aeiouEO!]{0,}[aeiouEO!]{1,})[mn]$", r"\1", word)
    word = re.sub(r"m$", "n", word)

    #loss of /h/
    word = re.sub(r"h", "", word)

    #/ns/ > /s/
    word = re.sub(r"ns", "s", word)

    #/rs/ > /ss/ except when preceded by /o/
    word = re.sub(r"(?<!o)rs", "ss", word)

    #final /er/, /or/ > /re/, /ro/
    word = re.sub(r"([eo])r$", r"r\1", word)

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
    word = re.sub(r"[dg]J", "G", word)

    #end WR
    return word

def toGIR(word, swap):

    #/kJ/ and /tJ/ merge to /tsJ/
    word = re.sub(r"kkJ", "ttJ", word)
    word = re.sub(r"[tk]J", "tsJ", word)

    #/k/ > /j/ before /s/ or /t/
    word = re.sub(r"k(?=[st])", "j", word)

    #first diphthongization: /E/ > /ie/, /O/ > /uo/ in open syllables or before /j/
    word = re.sub(r"!E(?=j|$|[tdkgpb][lr]|[^aeiouEOj]{0,1}[aeiouEO])", "j!E", word)
    word = re.sub(r"jj", "j", word)
    word = re.sub(r"!O(?=j|$|[tdkgpb][lr]|[^aeiouEOj]{0,1}[aeiouEO])", "w!O", word)

    #vowel loss before lenition
    if swap:

        #first unstressed vowel loss: pretonic vowels except /a/ (which becomes schwa)
        word = re.sub(r"([aeiouEO][^aeiouEO]{1,})[eiouEO](?=[^aeiouEO]{1,}!)", r"\1", word)

        #first lenition: voiced stops and unvoiced fricatives > voiced fricatives,
        #unvoiced stops > voiced stops, consonants before /r/ and /l/ lenited,
        #final /t/ and /d/ lenited
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

        #first lenition: voiced stops and unvoiced fricatives > voiced fricatives,
        #unvoiced stops > voiced stops, consonants before /r/ and /l/ lenited,
        #final /t/ and /d/ lenited
        lookup = {'b':'v', 'd':'D', 'g':'j', 'p':'b', 't':'d', 'k':'g', 'f':'v',
                's':'z', 'ts':'dz', 'pl':'bl', 'kl':'gl', 'gl':'jl', 'gn':'jn'}
        word = re.sub(r"(?<=[aeiouEO])[^aeiouEO!Jrwj]{1,2}(?=[aeiouEO!Jrwj])", lambda x: lookup.get(x.group(), x.group()), word)
        word = re.sub(r"(?<=[aeiouEO])d$", "D", word)
        word = re.sub(r"(?<=[aeiouEO])t$", "d", word)

        #/jn/, /nj/, /nJ/ > /N/ and /jl/, /gl/, /lJ/ > /L/
        word = re.sub(r"jn|nj|nJ", "N", word)
        word = re.sub(r"jl|gl|lJ", "L", word)

        #first unstressed vowel loss: pretonic vowels except /a/ (which becomes schwa)
        word = re.sub(r"([aeiouEO][^aeiouEO]{1,})[eiouEO](?=[^aeiouEO]{1,}!)", r"\1", word)

    #end GIR
    return word

def toPF(word):

    #/j/ when initial or stemming from /dJ/ or /gJ/ when preceded by a consonant becomes /dZ/
    word = re.sub(r"^j|(?<![aeiouEOw])G", "dZ", word)
    word = re.sub(r"G", "j", word)

    #/j/ palatalizes following consonant if present
    word = re.sub(r"(?<=j)([^aeiouEOw!])", r"\1J", word)

    #/pJ/ > /tS/, /bJ/ and /vJ/ > /dZ/, /mJ/ > /ndZ/
    word = re.sub(r"(?<=.)pJ(?=.)", "tS", word)
    word = re.sub(r"(?<=.)[bv]J(?=.)", "dZ", word)
    word = re.sub(r"(?<=.)mJ(?=.)", "ndZ", word)

    #palatized consonants eject preceding /j/ when open and a following /j/ when stressed open /a/ or /e/
    #special cases noted below

    #/tS/ and /dZ/ eject a following /j/ but not a preceding one
    word = re.sub(r"(tS|dZ)(?=![ae]($|[tdkgpb][lr]|[^aeiouEO]{0,1}[aeiouEO]))", r"\1j", word)

    #/ssJ/ and /dz/ eject preceding and following /j/
    word = re.sub(r"(ss|dz)J", r"j\1J", word)
    word = re.sub(r"(ss|dz)J(?=![ae]($|[tdkgpb][lr]|[^aeiouEO]{0,1}[aeiouEO]))", r"\1j", word)

    #/N/ and /L/ maintain their palatal quality

    #/rJ/ ejects a /j/, but it metathesizes when /a/ precedes
    word = re.sub(r"arJ", "jarJ", word)
    word = re.sub(r"(?<=[eiouEO])rJ", "jrJ", word)
    word = re.sub(r"(?<=[tdpbkg])rJ", "jrJ", word)
    word = re.sub(r"rJ(?=![ae]($|[tdkgpb][lr]|[^aeiouEO]{0,1}[aeiouEO]))", r"rj", word)

    #all other palatals
    word = re.sub(r"(?<!^)([^j].)J", r"j\1J", word)
    word = re.sub(r"J(?=![ae]($|[tdkgpb][lr]|[^aeiouEO]{0,1}[aeiouEO]))", r"j", word)
    word = re.sub(r"J", "", word)

    #second diphthongization: stressed open /e/ > /ej/, /o/ > /ow/, /a/ > /ae/ when not followed by /j/
    word = re.sub(r"!e(?=$|[tdkgpb][lr]|[^aeiouEOj]{0,1}[aeiouEO])", "!ej", word)
    word = re.sub(r"!o(?=$|[tdkgpb][lr]|[^aeiouEOj]{0,1}[aeiouEO])", "!ow", word)
    word = re.sub(r"!a(?=$|[tdkgpb][lr]|[^aeiouEOj]{0,1}[aeiouEO])", "!@", word)

    #?/aw/ > /O/, following /o/, /jo/, /go/, /ko/ fuse with /O/ to become /Ow/
    word = re.sub(r"(?<=aw)(o|jo|go|ko)", "w", word)
    word = re.sub(r"aw", "O", word)

    #second unstressed vowel loss: loss of unstressed vowels except /a/ (which becomes schwa) in final syllables
    word = re.sub(r"([^aeiouEO@]{0,}[aeiouEO@][^aeiouEO@!]{0,})[eiouEO@](?=[^aeiouEO@]{0,}$)", r"\1", word)

    #second lenition: same as first
    lookup = {'b':'v', 'd':'D', 'g':'j', 'p':'b', 't':'d', 'k':'g', 'f':'v',
            's':'z', 'ts':'dz', 'pl':'bl', 'kl':'gl', 'gl':'jl', 'gn':'jn'}
    word = re.sub(r"(?<=[aeiouEO])[^aeiouEO!Jrwj]{1,2}(?=[aeiouEO!Jrwj])", lambda x: lookup.get(x.group(), x.group()), word)
    word = re.sub(r"(?<=[aeiouEO])d$", "D", word)
    word = re.sub(r"(?<=[aeiouEO])t$", "d", word)

    #/ka/ > /tSa/, /ga/ > /dZa/
    word = re.sub(r"k(?=!{0,1}a)", "tS", word)
    word = re.sub(r"g(?=!{0,1}a)", "dZ", word)

    #unstressed /a/'s which weren't lost above become schwa (/e/)
    word = re.sub(r"([aeiouEO][^aeiouEO]{1,})a(?=[^aeiouEO]{1,}!)", r"\1e", word)
    word = re.sub(r"([^aeiouEO@]{0,}[aeiouEO@][^aeiouEO@!]{0,})a(?=[^aeiouEO@]{0,}$)", r"\1e", word)

    #/@/ > /E/ (/aj/ before nasal when not preceded by /j/), ?/aw/ > /O/
    word = re.sub(r"(?<!j)@(?=[nm])", "aj", word)
    word = re.sub(r"@", "E", word)
##    word = re.sub(r"aw", "O", word) #wikipedia says this step should be here, but it doesn't make much sense in this location

    #geminate stops become single stops
    word = re.sub(r"([pbtdkg])\1", r"\1", word)

    #final stops and fricatives become devoiced
    lookup = {'b':'p', 'd':'t', 'g':'k', 'v':'f', 'z':'s', 'D':'T'}
    word = re.sub(r"[bdgvzD](?=[^aeiouEO]{0,}$)", lambda x: lookup.get(x.group(), x.group()), word)

    #/dz/ > /z/ except at end
    word = re.sub(r"dz(?!$)", "z", word)

    #/t/ inserted between /N/ or /L/ and /s/
    word = re.sub(r"([NL])(?=s)", r"\1t", word)

    #depalatalization of /N/ and /L/ when final or following a consonant
    word = re.sub(r"N$", "jn", word)
    word = re.sub(r"(?<=[aeiouEO])N", "jn", word)
    word = re.sub(r"L$", "l", word)
    word = re.sub(r"(?<=[aeiouEO])L", "l", word)

    #/jEj/ > /i/, /wOj/ > /uj/
    word = re.sub(r"jEj", "i", word)
    word = re.sub(r"wOj", "uj", word)

    #end PF
    return word

def toOF(word):

    #loss of /f/, /p/, /k/ before final /s/, /t/
    word = re.sub(r"[fpk](?=[st]$)", "", word)

    #/u/ > /y/
    word = re.sub(r"u", "y", word)

    #nasalization of vowels before /n/ and /m/
    word = re.sub(r"(?<=[aeiouyEOjw])([nm])", r"~\1", word)

    #/ej/ > /oj/ (blocked by nasalization)
    word = re.sub(r"ej(?!~)", "oj", word)

    #/ow/ > /ew/ (blocked by nasalization and labial consonants)
    word = re.sub(r"ow(?![pbm~])", "ew", word)

    #/wo/ > /we/ (blocked by nasalization)
    word = re.sub(r"w(!{0,1})o(?!~)", r"w\1e", word)

    #lowering of /e~/ and /E~/ to /a~/ except when preceded or followed by /j/
    word = re.sub(r"([^j]!{0,1})[eE]~(?!j)", r"\1a~", word)

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

    #/l/ > /w/ before consonants (except in the sequence /lla/
    word = re.sub(r"l(?!la|[aeiouyEOjw])", "w", word)

    #/ew/, /we/ > /oe/
    word = re.sub(r"ew", "oe", word)
    word = re.sub(r"w(!{0,1})e", r"\1oe", word)

    #/oj/ > /we/
    word = re.sub(r"oj", "we", word)

    #/aj/ > /E/
    word = re.sub(r"aj", "E", word)

    #/e/ > /E/ in closed syllables
    word = re.sub(r"e(?=[^aeiouyEOwj~]{2,})", "E", word)

    #deaffrication: /ts/ > /s/, /tS/ > /S/, /dZ/ > /Z/
    word = re.sub(r"ts", "s", word)
    word = re.sub(r"tS", "S", word)
    word = re.sub(r"dZ", "Z", word)

    #end OF
    return word

def toMF(word):

    #?/Ow/ > /u/
    word = re.sub(r"Ow", "u", word)

    #/ej/ > /E/
    word = re.sub(r"ej", "E", word)

    #/u~/ and /o~/ > /O~/
    word = re.sub(r"[uo]~", "O~", word)

    #denasalization of nasal vowels when the following /n/ or /m/ is followed by a vowel
    word = re.sub(r"~(?=[nm][aeiouyEOjw!])", "", word)

    #deletion of /n/ and /m/ after remaining nasal vowels
    word = re.sub(r"~[mn]", "~", word)

    #loss of final consonants
    word = re.sub(r"[^aeiouyEOjw~]$", "", word)

    #/we/ > /wa/
    word = re.sub(r"w[eE]", "wa", word)

    #merging of /L/ with /j/
    word = re.sub(r"L", "j", word)

    #/i~/, /y~/ > /E~/
    word = re.sub(r"[iy]~", "E~", word)

    #end MF
    return word

evolve("mediet!a:tem", True)