import log_setup
import regex

log = log_setup.get_log()

def sub(pattern: str, repl: str, string: str, debug: bool = False) -> str:
    '''
    Wrapper for the regex.sub function which includes an optional debug argument.

    Parameters
    ----------
    pattern : str
        The regex pattern to match against.
    repl : str
        The replacement string.
    string : str
        The string in which to perform the replacement.
    debug : bool
        If True, will print the output of the substitution. 

    Returns
    -------
    str
        A new string with the substitution applied (if applicable).
    '''

    word = regex.sub(pattern, repl, string)
    if debug:
        log(word, stacklevel=2)
    return word

consonants: list[str] = []
vowels: list[str] = []

def reset() -> None:
    '''
    Resets the consonants and vowels to their initial (i.e., Latin) state.
    '''

    global consonants, vowels
    consonants = ['b', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'r', 's', 't', 'v', 'w', 'z']
    vowels = ['a', 'e', 'i', 'o', 'u']

def join(include: list[str], *exclude: str) -> str:
    '''
    Joins the elements of the list and returns a non-capturing regex group of the form '(?:e1|e2|e3...)'.

    Parameters
    ----------
    include : list[str]
        The list of elements to include in the group.
    *exclude : str
        Elements which should be excluded from the list.

    Returns
    -------
    str
        The non-capturing group.
    '''

    return '(?:' + '|'.join(i for i in include if i not in exclude) + ')'

def to_proto_western_romance(word: str, debug: bool = False) -> str:
    '''
    Simulates the sounds changes that occurred between Latin and Proto-Western Romance and returns the result.

    Parameters
    ----------
    word : str
        The word to apply the sound changes to.
    debug : bool
        If True, debug information will be output.

    Returns
    -------
    str
        The evolved word.
    '''
    
    global consonants, vowels

    # Introduction of short /i/ before initial /s/ + consonant.
    word = sub(f'^(?=s{join(consonants)})', 'i', word, debug)

    # Reduction of 10 vowels to 7. Unstressed /ɛ/, /ɔ/ raised to /e/, /o/, respectively.
    # SPECULATION: I'm not sure at the moment if this only affected /aj/ from <ae> or if it affected /ai/ + vowel clusters as well. Similarly for /oj/. For now I'm going to assume that it only affected <ae>/<oe>.
    word = sub('a:', 'a', word, debug)
    word = sub(f'aj(?={join(consonants)}|$)|e(?!:)', 'ɛ', word, debug)
    word = sub(f'oj(?={join(consonants)}|$)|e:|(?:i|y)(?!:)', 'e', word, debug)
    word = sub('(?:i|y):', 'i', word, debug)
    word = sub('o(?!:)', 'ɔ', word, debug)
    word = sub('u(?!:)|o:', 'o', word, debug)
    word = sub('u:', 'u', word, debug)
    word = sub('(?<!/)ɛ', 'e', word, debug)
    word = sub('(?<!/)ɔ', 'o', word, debug)

    vowels.extend(['ɛ', 'ɔ'])

    # Loss of final /m/ except in monosyllables, which becomes /n/.
    word = sub(f'(?<={join(vowels)}{join(consonants)}+/?{join(vowels)})m$', '', word, debug)
    word = sub('m$', 'n', word, debug)

    # Loss of /h/.
    word = sub('h', '', word, debug)

    consonants.remove('h')

    # /ns/ > /s/.
    word = sub('ns', 's', word, debug)

    # /rs/ > /ss/.
    # NOTE: There are some expections to this, but they aren't clearly defined, so I'm going to ignore them now.
    word = sub('rs', 'ss', word, debug)

    # Final /er/ > /re/, /or/ > /ro/.
    # SPECULATION: It's unspecified if this happens to /ɛr/ and /ɔr/ as well. I don't believe Latin ever allowed stress on the final syllable, and since /ɛ/ and /ɔ/ are only ever stressed, these combination might not be possible. As such, I'm going to ignore them for now. However, it doesn't indicate whether it happens with stressed /e/ and /o/ either, but again, since I don't believe Latin ever allowed stress to fall on the final syllable, this probably doesn't occur, so I'm going to assume it's only unstressed until I see an example indicating otherwise.
    word = sub('(e|o)r$', 'r\\1', word, debug)

    # Loss of unstressed interior syllables between /k/, /g/ and /r/, /l/.
    # SPECULATION: It's unspecified if this applies to /a/ or not, which typically resists being lost in other situations. For now, I'm going to assume that it's lost with the others.
    word = sub(f'(?<=k|g){join(vowels)}(?=r|l)', '', word, debug)

    # Reduction of /e/, /i/ in hiatus to /j/, followed by palatalization. /k/ geminates before palatalization.
    word = sub(f'(/?)(?:e|i)(?=/?{join(vowels)})', 'ʲ\\1', word, debug)
    word = sub('(?<!k)kʲ', 'kkʲ', word, debug)

    # /k/, /g/ palatalized before front vowels.
    word = sub('(?<=k|g)(/?(?:e|i|ɛ))', 'ʲ\\1', word, debug)

    # Initial /j/ and /dʲ/, /gʲ/, /z/ > /ɟ/.
    word = sub('^j|dʲ|gʲ|z', 'ɟ', word, debug)

    # TODO: Some stuff happens with /w/ at some point, but not sure where at the moment. Need to check other sources.

    consonants.append('ɟ')

    return word

def to_proto_gallo_ibero_romance(word: str, debug: bool = False) -> str:
    '''
    Simulates the sounds changes that occurred between Latin and Proto-Gallo-Ibero-Romance and returns the result.

    Parameters
    ----------
    word : str
        The word to apply the sound changes to.
    debug : bool
        If True, debug information will be output.

    Returns
    -------
    str
        The evolved word.
    '''
    
    global consonants, vowels

    # /kʲ/, /tʲ/ merge to /ʦʲ/.
    word = sub('kkʲ', 'ttʲ', word, debug)
    word = sub('(?:k|t)ʲ', 'ʦʲ', word, debug)

    consonants.append('ʦ')

    # /kt/ > /jt/, /ks/ > /js/.
    word = sub('k(?=s|t)', 'j', word, debug)

    # Stressed open /ɛ/ > /jɛ/, /ɔ/ > /wɔ/. This also happens in closed syllables before /j/.
    word = sub(f'ɛ(?={join(consonants)}+ʲ?{join(vowels)}|j)', 'jɛ', word, debug)
    word = sub(f'ɔ(?={join(consonants)}+ʲ?{join(vowels)}|j)', 'wɔ', word, debug)

    return word

def evolve(word: str, debug: bool = False) -> str:
    '''
    Simulates the sounds changes that occurred between Latin and French and returns the result.

    To ensure the word is converted as expected, use the following conventions. In general, the word should be written phonetically, rather than as it's spelled in Latin.
        - Stress falls on the penultimate syllable unless short, in which case it falls on the antepenultimate if possible.
        - Note that plosive + liquid clusters are considered short when determining the position of stress.
        - Mark stress with a '/' before the stressed vowel, like so: 'mediet/a:tem'.
        - Mark long vowels with a ':' after the vowel, like so: 'mediet/a:tem'.
        - Replace 'y' with 'i', 'ae' with 'aj', 'oe' with 'oj'.
        - Replace 'i' in hiatus with 'j' and 'u' in hiatus with 'w'.
        - Replace 'c' with 'k', 'qu' with 'kw', and 'x' with 'ks'.

    Parameters
    ----------
    word : str
        The word to apply the sound changes to.
    debug : bool
        If True, debug information will be output.

    Returns
    -------
    str
        The evolved word.
    '''

    reset()
    word = to_proto_western_romance(word, debug)
    return word

if __name__ == '__main__':
    word = evolve('per', True)
    print(word)