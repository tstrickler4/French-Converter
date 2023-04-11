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
        If True, will log the output of the substitution. 

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

    # Substitute "kʷ" for /kw/ and "gʷ" for /gw/. The velarized forms of /k/ and /g/ evolve differently from regular /k/ and /g/, but they're difficult to type, so this substitution should help.
    word = sub('kw', 'kʷ', word, debug)
    word = sub('gw', 'gʷ', word, debug)

    consonants.extend(['kʷ', 'gʷ'])

    # Dissimilation of multiple /kw/s.
    word = sub('kʷ(?=.+kʷ)', 'k', word, debug)

    # Introduction of short /i/ before initial /s/ + consonant.
    word = sub(f'^(?=s{join(consonants)})', 'i', word, debug)

    # Reduction of 10 vowels to 7. Unstressed /ɛ/, /ɔ/ raised to /e/, /o/, respectively.
    # TODO: I'm not sure at the moment if this only affected /aj/ from <ae> or if it affected /ai/ + vowel clusters as well. Similarly for /oj/. For now I'm going to assume that it only affected <ae>/<oe>.
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
    # TODO: Based on examples, this appears to have also happened to final /n/ in words borrowed from Gaulish.
    word = sub(f'(?<={join(vowels)}{join(consonants)}*/?{join(vowels)})(?:m|n)$', '', word, debug)
    word = sub('m$', 'n', word, debug)

    # Loss of /h/.
    word = sub('h', '', word, debug)

    # I'm going to leave /h/ in the list for the time being as it can reappear in Germanic borrowings in later periods.
    # consonants.remove('h')

    # /ns/ > /s/.
    word = sub('ns', 's', word, debug)

    # /rs/ > /ss/.
    # TODO: There are some expections to this, but they aren't clearly defined, so I'm going to ignore them now.
    word = sub('rs', 'ss', word, debug)

    # Final /er/ > /re/, /or/ > /ro/.
    # TODO: It's unspecified if this happens to /ɛr/ and /ɔr/ as well. I don't believe Latin ever allowed stress on the final syllable, and since /ɛ/ and /ɔ/ are only ever stressed, these combinations might not be possible. As such, I'm going to ignore them for now. However, it doesn't indicate whether it happens with stressed /e/ and /o/ either, but again, since I don't believe Latin ever allowed stress to fall on the final syllable, this probably doesn't occur, so I'm going to assume it's only unstressed until I see an example indicating otherwise. I also suspect that this doesn't happen in single syllable words, since Latin <per> > French <par>.
    word = sub(f'(?<={join(vowels)}{join(consonants)}+)(e|o)r$', 'r\\1', word, debug)

    # Loss of unstressed interior syllables between /k/, /g/ and /r/, /l/.
    # TODO: It's unspecified if this applies to /a/ or not, which typically resists being lost in other situations. For now, I'm going to assume that it's lost with the others.
    word = sub(f'(?<=k|g){join(vowels)}(?=r|l)', '', word, debug)

    # Reduction of /e/, /i/ in hiatus to /j/, followed by palatalization. Stress shifts forward. /k/ geminates before palatalization.
    word = sub(f'(/?)(?:e|i)(?=/?{join(vowels)})', 'j\\1', word, debug)
    word = sub(f'(?<={join(consonants)})j', 'ʲ', word, debug)
    word = sub('(?<!k)kʲ', 'kkʲ', word, debug)

    # Reduction of /o/, /u/ in hiatus to /w/. Stress shifts backward if possible. Initial /w/ > /v/.
    # TODO: Not gonna lie, I'm purely guessing on the "initial /w/ > /v/" part based on some examples that I've seen, but I have no idea how to explain certain later changes otherwise.
    word = sub(f'({join(vowels)})(/?)(?:o|u)(?=/?{join(vowels)})', '\\1\\2w', word, debug)
    word = sub(f'(/?)(?:o|u)(?=/?{join(vowels)})', 'w\\1', word, debug)
    word = sub('^w', 'v', word, debug)

    # /k/, /g/ palatalized before front vowels.
    word = sub('(?<=k|g)(/?(?:e|i|ɛ))', 'ʲ\\1', word, debug)

    # Initial /j/ and /dʲ/, /gʲ/, /z/ > /ɟ/.
    word = sub('^j|dʲ|gʲ|z', 'ɟ', word, debug)

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

    # /nkt/ > /nt/, /nks/ > /ns/, /kt/ > /jt/, /ks/ > /jss/, /gm/ > /wm/.
    # TODO: I think the /ks/ case becomes /jss/ as opposed to /js/ as suggested because it maintains an /s/ in French, rather than leniting to /z/, so it must've been long.
    # word = sub('(?<=n)k(?=s|t)', '', word, debug)
    word = sub('k(?=s)', 'js', word, debug)
    word = sub('k(?=t)', 'j', word, debug)
    word = sub('gm', 'wm', word, debug)

    # First diphthongization: stressed open /ɛ/ > /jɛ/, /ɔ/ > /wɔ/. This also happens in closed syllables before /j/.
    # TODO: Based on examples, it appears that /ɔ/ remains before nasals.
    word = sub(f'/ɛ(?={join(consonants)}ʲ?{join(vowels)}|j)', 'j/ɛ', word, debug)
    word = sub(f'(?<!w)/ɔ(?=(?:{join(consonants, "n", "m")}|(?:p|b|t|d|g|k)(?:r|l))ʲ?{join(vowels)}|j)', 'w/ɔ', word, debug)

    # /a/ > /ɔ/ before back rounded vowels or /g/ + back rounded vowels. This also happens to /aw/ before /g/ + back rounded vowels.
    # TODO: Based on examples, I think the /a/ might need to be stressed. If you allow both stressed and unstressed /a/, you get contradicting examples. I'm not entirely sure on this though, so I might change it later.
    word = sub(f'/a(?=(?:o|u|ɔ)|w{join(vowels)}|(?:g|k)(?:o|u|ɔ))', '/ɔ', word, debug)
    word = sub(f'aw(?=(?:g|k)/?(?:o|u|ɔ))', 'ɔ', word, debug)
    word = sub(f'(?<={join(vowels, "ɔ")})w(?=/?{join(vowels)})', 'v', word, debug)

    # First lenition.
    # TODO: Based on examples, I'm guessing that preceding diphthongs still count.
    word = sub(f'(?<={join(vowels)}w?j?)(?:b|f)(?=r?ʲ?/?{join(vowels)})', 'v', word, debug)
    word = sub(f'(?<={join(vowels)}w?j?)p(?=(?:r|l)?ʲ?/?{join(vowels)})', 'b', word, debug)
    word = sub(f'(?<={join(vowels)}w?j?)d(?=r?ʲ?/?{join(vowels)}|$)', 'ð', word, debug)
    word = sub(f'(?<={join(vowels)}w?j?)t(?=r?ʲ?/?{join(vowels)}|$)', 'd', word, debug)
    word = sub(f'(?<={join(vowels)}w?j?)s(?=ʲ?/?{join(vowels)})', 'z', word, debug)
    word = sub(f'(?<={join(vowels)}w?j?)ʦ(?=ʲ?/?{join(vowels)})', 'ʣ', word, debug)
    word = sub(f'(?<=ɔ)(?:g|k)(?=/?(?:o|u|ɔ|w))', 'w', word, debug)
    word = sub(f'(?<={join(vowels)})g(?=/?(?:o|u|ɔ))', '', word, debug)
    word = sub('(?<=u|w)g(?=/?a)', '', word, debug)
    word = sub('(?<=o|ɔ)g(?=/?a)', 'v', word, debug)
    word = sub(f'(?<={join(vowels)}w?j?)g(?=(?:n|r|l)?ʲ?/?{join(vowels)})', 'j', word, debug)
    word = sub(f'(?<={join(vowels)}w?j?)k(?=(?:r|l)?ʲ?/?{join(vowels)})', 'g', word, debug)
    word = sub(f'(?<=i|e|ɛ)kʷ(?=/?{join(vowels)})', 'w', word, debug)

    consonants.extend(['ð', 'ʣ'])

    # Formation of palatal new palatal consonants: /ɲ/, /ʎ/.
    word = sub('jn|nj|nɟ|nʲ', 'ɲ', word, debug)
    word = sub('jl|gl|lʲ', 'ʎ', word, debug)

    consonants.extend(['ɲ', 'ʎ'])

    # First vowel loss: loss of pretonic vowels except /a/ when not initial. This sporadically occurs before the first lenition.
    # TODO: Based on examples, it looks like initial vowels are then reduced to /ə/.
    word = sub(f'(?<={join(vowels)}{join(consonants)}*){join(vowels, "a")}(?={join(consonants)}*(?:ʲ|j|w)?/{join(vowels)})', '', word, debug)

    # TODO: Consonant clusters are reduced here, but the mechanisms are complicated. Ignoring it for now.

    return word

def to_early_old_french(word: str, debug: bool = False) -> str:
    '''
    Simulates the sounds changes that occurred between Latin and Early Old French and returns the result.

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

    # /ɟ/ when initial and following a consonant become /ʤ/. All others become /j/.
    word = sub(f'^ɟ|(?<={join(consonants, "w", "j")}ʲ?)ɟ', 'ʤ', word, debug)
    word = sub('ɟ', 'j', word, debug)

    consonants.remove('ɟ')

    # /j/ palatalizes following consonants.
    # TODO: It's unspecified if the palatalization passes through clusters. For now I'll assume that that situation doesn't occur.
    word = sub(f'j({join(consonants, "ɲ", "ʎ")}(?!ʲ))', 'j\\1ʲ', word, debug)

    # Consonants depalatalize and eject a /j/ (sometimes two).
    word = sub(f'(?<={join(vowels)})(?:b|v)ʲ(?=/?{join(vowels)})', 'ʤ', word, debug)
    word = sub(f'(?<={join(vowels)})(?:p|f)ʲ(?=/?{join(vowels)})', 'ʧ', word, debug)
    word = sub(f'(?<={join(vowels)})mʲ(?=/?{join(vowels)})', 'nʤ', word, debug)
    word = sub(f'arʲ(?=/?{join(vowels)})', 'jarʲ', word, debug)
    word = sub(f'(?<={join(vowels)})((?:{join(consonants, "r")}|ss)ʲ)(?=/?{join(vowels)})', 'j\\1', word, debug)
    word = sub(f'({join(consonants)}ʲ|ʤ|ʧ)(?=/(?:a|æ|e)j?w?(?:{join(consonants)}ʲ?{join(vowels)}|$))', '\\1j', word, debug)
    word = sub('ʲ', '', word, debug)

    consonants.append('ʧ')

    # Second diphthongization: stressed open /e/ > /ej/, /o/ > /ow/, /a/ > /æ/ when not followed by /j/.
    # TODO: Based on examples, it appears that /o/ remains before nasals, and /a/ remains before /ɲ/.
    word = sub(f'/e(?=(?:{join(consonants, "j")}|(?:p|b|t|d|g|k)(?:r|l)){join(vowels)}|$)', '/ej', word, debug)
    word = sub(f'/o(?=(?:{join(consonants, "j", "n", "m", "ɲ")}|(?:p|b|t|d|g|k)(?:r|l)){join(vowels)}|$)', '/ow', word, debug)
    word = sub(f'/a(?=(?:{join(consonants, "j", "ɲ")}|(?:p|b|t|d|g|k)(?:r|l)){join(vowels)}|$)', '/æ', word, debug)

    vowels.append('æ')

    # /ɔ/ combines with back rounded vowels to produce /ɔw/.
    word = sub('(?<=ɔ)g?(?:o|u|ɔ)', 'w', word, debug)

    # TODO: I originally included these steps as part of the second lenition below, but based on examples, these need to happen before the posttonic vowel loss.
    word = sub(f'(?<={join(vowels)})g(?=/?(?:o|u|ɔ))', '', word, debug)
    word = sub('(?=o|u|ɔ|w)g(?=/?a)', '', word, debug)

    # Loss of posttonic vowels except /a/, which reduces to /ə/. Remaining final vowels except /a/ reduced to /ə/.
    # TODO: Because the vocalization of /l/ needed to occur after the vowel loss, this step continues with the reduction to /ə/ after the vocalization step below.
    word = sub(f'(?<=/{join(vowels)}{join(consonants)}*){join(vowels, "a")}', '', word, debug)

    # Vocalization of /l/ before consonants began in the ninth century with /l/ > /ɫ/. It's not specified exactly when, but it for certain had to have begun before the loss of gemination as vocalization occurred in /ll/ as well except before /a/. Vocalization won't complete until much later, however, when /ɫ/ > /w/.
    # TODO: Based on examples, it looks like this affects /ʎ/ before consonants as well.
    word = sub('lla', 'la', word, debug)
    word = sub('ll', 'ɫɫ', word, debug)
    word = sub(f'(?:l|ʎ)(?={join(consonants, "j", "w")})', 'ɫ', word, debug)

    consonants.append('ɫ')

    # This is the continuation of the vowel loss mentioned above.
    word = sub(f'(?<=/{join(vowels)}{join(consonants)}*){join(vowels)}', 'ə', word, debug)

    vowels.append('ə')

    # TODO: Consonant clusters may be reduced here again.
    # /tl/ > /kl/.
    word = sub('tl', 'kl', word, debug)

    # Second lenition.
    # TODO: Based on examples, I'm guessing preceding diphthongs still count.
    word = sub(f'(?<={join(vowels)}w?j?)(?:b|f)(?=r?/?{join(vowels)})', 'v', word, debug)
    word = sub(f'(?<={join(vowels)}w?j?)p(?=(?:r|l)?/?{join(vowels)})', 'b', word, debug)
    word = sub(f'(?<={join(vowels)}w?j?)d(?=r?/?{join(vowels)}|$)', 'ð', word, debug)
    word = sub(f'(?<={join(vowels)}w?j?)t(?=r?/?{join(vowels)}|$)', 'd', word, debug)
    word = sub(f'(?<={join(vowels)}w?j?)s(?=/?{join(vowels)})', 'z', word, debug)
    word = sub(f'(?<={join(vowels)}w?j?)ʦ(?=/?{join(vowels)})', 'ʣ', word, debug)
    word = sub(f'(?<={join(vowels)}w?j?)g(?=(?:n|r|l)?/?{join(vowels)})', 'j', word, debug)
    word = sub(f'(?<={join(vowels)}w?j?)k(?=(?:r|l)?/?{join(vowels)})', 'g', word, debug)
    word = sub(f'(?<=i|e|ɛ|æ)kʷ(?=/?{join(vowels)})', 'w', word, debug)

    # Palatalization of /k/ > /ʧ/, /g/ > /ʤ/ before /a/.
    # TODO: Although unspecified. I suspect this happened before /æ/ as well. It looks like this also affected /kk/ and /gg/.
    word = sub('k?k(?=/?(?:a|æ))', 'ʧ', word, debug)
    word = sub('g?g(?=/?(?:a|æ))', 'ʤ', word, debug)

    consonants.append('ʧ')
    
    # /æ/ > /jɛ/ after /ʧ/ or /ʤ/ and followed by a nasal or /j/, or /aj/ before nasals if not preceeded by /j/, otherwise /ɛ/.
    # TODO: The addition of /j/ after /ʧ/ or /ʤ/ seems to have been universal, but by Modern French, based on examples, the /j/ only remains if followed by a nasal. Compare the evolution of <cher> vs <chien>.
    word = sub('(?<=ʧ|ʤ)/æ(?=(?:j|n|m|ɲ))', 'j/ɛ', word, debug)
    word = sub('(?<!j)/æ(?=(?:n|m|ɲ))', '/aj', word, debug)
    word = sub('æ', 'ɛ', word, debug)

    vowels.remove('æ')

    # /aw/ > /ɔ/.
    word = sub('aw', 'ɔ', word, debug)

    # Loss of gemination accept for /rr/.
    word = sub(f'({join(consonants, "r")})\\1', '\\1', word, debug)

    # Final stops and fricatives devoiced.
    # TODO: I'm assuming this also happens to affricates based on /ʣ/ not being listed in the deaffrication step which happens later in combination with the following step in which it deaffricates to /z/. Otherwise, this sound would still exist in modern French.
    word = sub('b$', 'p', word, debug)
    word = sub('v$', 'f', word, debug)
    word = sub('d$', 't', word, debug)
    word = sub('ð$', 'θ', word, debug)
    word = sub('z$', 's', word, debug)
    word = sub('ʣ$', 'ʦ', word, debug)
    word = sub('g$', 'k', word, debug)

    consonants.append('θ')

    # /ʣ/ > /z/ when not final.
    word = sub('ʣ(?!$)', 'z', word, debug)

    consonants.remove('ʣ')

    # /t/ inserted between /ɲ/, /ʎ/ and following /s/.
    word = sub('(ɲ|ʎ)s', '\\1ʦ', word, debug)

    # Depalatalization of /ɲ/, /ʎ/ when following a consonant or final.
    # TODO: Based on examples, it looks like it happens to /ɲ/ when followed by consonants also.
    word = sub(f'ɲ(?={join(consonants)})', 'jn', word, debug)
    word = sub(f'(?<={join(consonants, "j")})ɲ|(?<!j)ɲ$', 'jn', word, debug)
    word = sub(f'(?<={join(consonants)})ʎ|ʎ$', 'l', word, debug)

    # /jaj/, /jɛj/, /jej/ > /i/ and /wɔj/ > /uj/.
    word = sub('j(/?)(?:a|ɛ|e)j', '\\1i', word, debug)
    word = sub('w(/?)ɔj', '\\1uj', word, debug)

    # Final /a/ > /ə/.
    # TODO: I think this occurs for unstressed /a/s in other places too, but need examples.
    word = sub('a$', 'ə', word, debug)

    return word

def to_old_french(word: str, debug: bool = False) -> str:
    '''
    Simulates the sounds changes that occurred between Latin and Old French and returns the result.

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

    # Loss of /f/, /p/, /k/ before final /s/, /t/.
    word = sub('(?:f|p|k)(?=s$|t$)', '', word, debug)

    # Nasalization of low vowels before all nasals.
    word = sub('((?:a|e|o|ɛ|ɔ|ɑ)(?:w|j)?)(?=m|n|ɲ)', '\\1~', word, debug)

    # /ej/ > /oj/ (blocked by nasalization).
    word = sub('ej(?!~)', 'oj', word, debug)

    # /ow/ > /ew/ (blocked by labials and nasalization).
    word = sub('ow(?!p|b|v|f|m|~)', 'ew', word, debug)

    # /wɔ/ > /wɛ/ (blocked by nasalization).
    word = sub('w(/?)ɔ(?!~)', 'w\\1ɛ', word, debug)

    # /a/ > /ɑ/ before /s/ or /z/.
    word = sub('a(?=s|z)', 'ɑ', word, debug)

    vowels.append('ɑ')

    # Loss of /θ/ and /ð/. When it results in a hiatus of /a/ with a following vowel, the /a/ becomes /ə/.
    word = sub('θ|ð', '', word, debug)
    word = sub(f'a(?={join(vowels)})', 'ə', word, debug)

    consonants = [i for i in consonants if i not in ('θ', 'ð')]

    # /kʷ/ > /k/ and /gʷ/ > /g/.
    word = sub('kʷ', 'k', word, debug)
    word = sub('gʷ', 'g', word, debug)

    consonants = [i for i in consonants if i not in ('kʷ', 'gʷ')]

    # /u/ > /y/.
    word = sub('u', 'y', word, debug)

    vowels.append('y')

    # Merge of /e~/ and /ɛ~/ to /a~/, but not in /jɛ~/ or /ej~/.
    word = sub('(?<!j)/(?:e|ɛ)(?=~)', '/a', word, debug)
    word = sub('(?<!j|/)(?:e|ɛ)(?=~)', 'a', word, debug)

    # Nasalization of high vowels before all nasals.
    word = sub('((?:i|u|y)(?:w|j)?)(?=m|n|ɲ)', '\\1~', word, debug)

    # Reduction of /e/ and /ɛ/ in hiatus to /ə/.
    word = sub(f'(?:e|ɛ)(?=/{join(vowels)}|(?:w|j)/{join(vowels)})', 'ə', word, debug)

    # Final /rn/, /rm/ > /r/.
    # TODO: What about /rɲ/?
    word = sub('r(?:n|m)$', 'r', word, debug)

    return word

def to_late_old_french(word: str, debug: bool = False) -> str:
    '''
    Simulates the sounds changes that occurred between Latin and Late Old French and returns the result.

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

    # /o/ > /u/.
    word = sub('o(?!j)', 'u', word, debug)

    # /ɔ/ > /o/ before /s/ or /z/.
    word = sub('ɔ(?=s|z)', 'o', word, debug)

    # /wɛ/, /ew/ > /œ/, but /ø/ before /s/, /z/, or /t/ and /jœ/ before /ɫ/ when not after a labial or velar.
    word = sub('w(/?)ɛ|ew', '\\1œ', word, debug)
    word = sub('(?<!m|p|b|v|f|k|g)/œ(?=ɫ)', 'j/œ', word, debug)
    word = sub('(?<!m|p|b|v|f|k|g|/)œ(?=ɫ)', 'jœ', word, debug)
    word = sub('œ(?=s|z|t)', 'ø', word, debug)

    vowels.extend(['ø', 'œ'])

    # Stress shift to second element of diphthongs.
    # TODO: I'll probably add more as I encounter them.
    word = sub('(/?)yj', 'ɥ\\1i', word, debug)
    word = sub(f'y(?=/?{join(vowels)})', 'ɥ', word, debug)

    consonants.append('ɥ')

    # /oj/, /ɔj/ > /wɛ/.
    word = sub('(/?)(?:o|ɔ)j', 'w\\1ɛ', word, debug)

    # /aj/ > /ɛ/.
    # TODO: I'm marking /ɛ/ which evolve from /aj/ with "E", as it apparently evolves differently from other /ɛ/s.
    word = sub('aj', 'E', word, debug)

    vowels.append('E')

    # Closed /e/ > /ɛ/.
    word = sub(f'e(?={join(consonants, "j", "ɫ")}{{2,}}|{join(consonants, "j", "ɫ")}$)', 'ɛ', word, debug)

    # Deaffrication.
    word = sub('ʦ', 's', word, debug)
    word = sub('ʧ', 'ʃ', word, debug)
    word = sub('ʤ', 'ʒ', word, debug)

    consonants = [i for i in consonants if i not in ('ʦ', 'ʧ', 'ʤ')]
    consonants.extend(['ʃ', 'ʒ'])

    # /ɫ/ > /w/.
    word = sub(f'ɫ', 'w', word, debug)

    # Loss of /s/ before consonants with lengthening of preceeding vowel.
    word = sub(f's(?={join(consonants, "j", "w", "ɥ")})', ':', word, debug)

    return word

def to_middle_french(word: str, debug: bool = False) -> str:
    '''
    Simulates the sounds changes that occurred between Latin and Middle French and returns the result.

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

    # /aw/ > /o/ (from previous /aɫ/).
    # TODO: I'm going to assume the other vowel + /w/ (from vowel + /ɫ/) combinations take affect here as well.
    word = sub('aw', 'o', word, debug)
    word = sub('(?<!j)/ɛw', '/o', word, debug)
    word = sub('(?<!j|/)ɛw', 'o', word, debug)
    word = sub('(?:ɛ|e|œ)w', 'œ', word, debug)
    word = sub('œ(?=s|z|t)', 'ø', word, debug)
    word = sub('uw', 'u', word, debug)

    # /ej/ > /ɛ/.
    word = sub('ej', 'ɛ', word, debug)

    # Nasal /u~/ > /ɔ~/.
    word = sub('u~', 'ɔ~', word, debug)

    # Denasalization of open vowels.
    word = sub(f'~(?=(?:n|m|ɲ)(?:/?{join(vowels)}|j|w))', '', word, debug)

    # Loss of nasals after nasal vowels.
    word = sub('(?<=~)(?:n|m|ɲ)', '', word, debug)

    return word

def to_early_modern_french(word: str, debug: bool = False) -> str:
    '''
    Simulates the sounds changes that occurred between Latin and Early Modern French and returns the result.

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

    # Loss of long vowels.
    word = sub(':', '', word, debug)

    # Loss of final consonants. This actually started in Middle French, but it was based on external sandhi.
    # TODO: Wikipedia isn't very specific regarding which consonants are lost. Based on examples, it looks like /r/, /l/, /f/ and /k/ remain. Beyond that, I need to refer to other sources. For now, I'm going to just assume all other consonants except those that form diphthongs. Addtionally, based on examples, /l/ does appear to be lost after high vowels, however, I've seen one example, /nu:llum/ > /nyl/, which suggests it's not always true. One source suggested that examples like this are the exception, based on influence from Latin.
    word = sub(f'{join(consonants, "f", "k", "r", "l", "j", "w", "ɥ")}+$', '', word, debug)
    word = sub('(?<=i|u|y)l$', '', word, debug)

    # /wɛ/ > /wa/ or sometimes /ɛ/.
    # TODO: Wikipedia doesn't indicate when it becomes /ɛ/. I need to check other sources. Based on examples, it also appears to be blocked by nasalization.
    word = sub('w(/?)ɛ(?!~)', 'w\\1a', word, debug)

    # /ɔw/ > /u/.
    word = sub('ɔw', 'u', word, debug)

    # Loss of /h/. It reemerged in borrowings from Germanic languages.
    word = sub('h', '', word, debug)

    consonants.remove('h')

    return word

def to_modern_french(word: str, debug: bool = False) -> str:
    '''
    Simulates the sounds changes that occurred between Latin and Modern French and returns the result.

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

    # /r/ > /ʁ/.
    word = sub('r', 'ʁ', word, debug)

    consonants.remove('r')
    consonants.append('ʁ')

    # /ʎ/ merges with /j/.
    word = sub('ʎ', 'j', word, debug)

    # Loss of /ə/ unless it results in an invalid consonant cluster.
    # TODO: Handling all possible resulting consonant clusters sounds like a huge pain, so for now I'm going to just remove all of them and then chalk it up to "use your best judgement".
    word = sub('ə', '', word, debug)

    # Lowering of nasal /i~/, /e~/ to /ɛ~/. In the 20th century, this has started to happen with /y~/, which originally shifted to /œ~/. As such, I've implemented this change as well.
    word = sub('(?:i|e|y)(?=~)', 'ɛ', word, debug)

    # Merge of /ɑ/ with /a/.
    word = sub('ɑ', 'a', word, debug)

    # Nasal /a~/ shifts to /ɑ~/.
    word = sub('a~', 'ɑ~', word, debug)

    # Final /ɔ/ > /o/, /ɛ/ > /e/, /œ/ > /ø/.
    word = sub('ɔ$', 'o', word, debug)
    word = sub('ɛ$', 'e', word, debug)
    word = sub('œ$', 'ø', word, debug)
    word = sub('E', 'ɛ', word, debug)

    vowels.remove('E')

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
    word = to_proto_gallo_ibero_romance(word, debug)
    word = to_early_old_french(word, debug)
    word = to_old_french(word, debug)
    word = to_late_old_french(word, debug)
    word = to_middle_french(word, debug)
    word = to_early_modern_french(word, debug)
    word = to_modern_french(word, debug)
    return word
