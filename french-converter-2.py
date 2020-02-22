"""
This is version 2 of a project developed to simulate the sound changes during
the development of French from Latin. Changes from version 1 mainly incorporate
the IPA to provide a more accurate result. Like version 1, however, it is still
in no way close to perfect as there are many exceptions which seem to break the
expected rules (just look at my test cases at the end for several examples).
Note that it is not intended to simulate the orthography, just the phonology. If
you want a hint at how the final result might look orthographically, refer to
how it looked during the Old French stage, as that seems to be where much of the
orthography developed. It's not always accurate, however, as there are many
instances of spelling reform adding in characters to better approximate how it
was originally spelled in Latin, but it should get you pretty close.

Most of the information stems from the "Phonological History of French"
Wikipedia page. I also refer to "The Interaction of Vowel Deletion and Syllable
Structure Contraints" by Moira Taylor in some cases, as she provides a much
more in depth look at syncope and apocope in the French language than the
Wikipedia page does.

The Wikipedia page is also just not very detailed in general. It also
contradicts itself in many places and seems to mix up orthography and the IPA
quite often. I tried my best to work with what I was given, but it required a
lot of guess work, speculation, and reading between the lines. Throughout the
code, I included comments detailing many of the choices I made and why I made
them.

Some notes for use:
    1. You'll notice that the functions for each of the stages of development
       have two optional parameters: showprev and showall. If showprev is set to
       True, it will run and print all previous stages. If showall is set to
       True, it will run each individual sound change mentioned during that
       stage only. Probably not the best parameter name since the "all" part
       might lead to a little confusion, but it is what it is.
    2. Regarding the format of the input, you can indicate long vowels by
       following them with a ":", and you can indicate stressed vowels by
       preceding them with a "!". Note that the "!" DOES NOT precede the entire
       syllable, just the vowel.
    3. For the most part I use the IPA throughout the project. There are a few
       exceptions, however. "K" and "G" are identical to /k/ and /g/, but they
       stem from Latin "qu" and "gu", which were resistant to certain sound
       changes that affected regular /k/ and /g/. "J" is identical to /j/, but
       it stems from /dʲ/ or /gʲ/, which were similarly resistant to sound
       changes that affected regular /j/. Lastly, "E" is identical to /ɛ/, but
       stems from /aj/, again used for similar reasons.
    4. I use the character "ñ" to indicate that the previous vowel is nasalized,
       as using the diacritic is difficult to work with in code.
    5. Regarding the output, there may be some missing schwas, as it is
       difficult to predict possible resulting consonant clusters and when and
       where schwas need to be inserted. As such, if your heart says there
       should be a schwa in there, it's probably right.

Let me know if you find any bugs or have any information on how I might improve
the progam.

Enjoy!
"""

import re

def printif(show, val):
    if show:
        print(val, end=" ")

def setup(word):
    # simplify orthography
    new_word = word
    new_word = re.sub(r"c", r"k", new_word)
    # I use <K> for /qu/ and <G> for /gu/ because these are pronounced as /k/
    # and /g/, but are resistant to changes which affect regular /k/ and /g/
    new_word = re.sub(r"qu", r"K", new_word)
    new_word = re.sub(r"gu(?=!?[aeiouy])", r"G", new_word)
    new_word = re.sub(r"x", r"ks", new_word)
    new_word = re.sub(r"ae", r"aj", new_word)
    new_word = re.sub(r"oe", r"oj", new_word)
    new_word = re.sub(r"(?<=[aeiouy:])i", r"j", new_word)
    new_word = re.sub(r"(!?)i(?=[aeiouy!])", r"j\1", new_word)
    new_word = re.sub(r"(?<=[aeiouy:])u(!?)(?=[aeiouy!])", r"w", new_word)
    new_word = re.sub(r"au", r"aw", new_word)
    return new_word



def to_proto_western_romance(word, showprev=True, showsteps=False):

    new_word = setup(word)
    if showprev:
        print(new_word, end=" ")

    # introduction of short /i/ at beginning before /s/ + C
    new_word = re.sub(r"^(s[bdfgGhkKlmnprstvz])", r"i\1", new_word)
    printif(showsteps, new_word)

    # reduction of ten vowels to seven
    new_word = re.sub(r"a:", r"a", new_word)
    new_word = re.sub(r"aj|e(?!:)", r"ɛ", new_word)
    new_word = re.sub(r"oj|e:|i(?!:)|y(?!:)", r"e", new_word)
    new_word = re.sub(r"i:|y:", r"i", new_word)
    new_word = re.sub(r"o(?!:)", r"ɔ", new_word)
    new_word = re.sub(r"o:|u(?!:)", r"o", new_word)
    new_word = re.sub(r"u:", r"u", new_word)
    printif(showsteps, new_word)

    # unstressed /ɛ/, /ɔ/ > /e/, /o/
    # SPECULATION: Wikipedia mentions that at some point in the development of
    # Proto-Western-Romance, unstressed /ɛ/, /ɔ/ > /e/, /o/. It it unspecified
    # exactly when this occurred, however, so I will include it here for now.
    # Should the need arise, it may need to be moved elsewhere.
    new_word = re.sub(r"(?<!!)ɛ", r"e", new_word)
    new_word = re.sub(r"(?<!!)ɔ", r"o", new_word)
    printif(showsteps, new_word)

    # loss of final /m/ except in monosyllables
    # SPECULATION: This appears to've also happened to final /n/.
    new_word = re.sub(r"([bdfgGhjkKlmnprstvwz!]*[aeiouɛɔ][bdfgGhjkKlmnprstvwz!]+[aeiouɛɔ])[mn]$", r"\1", new_word)
    printif(showsteps, new_word)

    # loss of /h/
    # SPECULATION: It appears initial /h/ prevents future /j/ from developing to
    # /dʒ/. As such, I'll leave initial /h/ until later.
    new_word = re.sub(r"(?<!^)h", r"", new_word)
    printif(showsteps, new_word)

    # /ns/ > /s/
    new_word = re.sub(r"ns", r"s", new_word)
    printif(showsteps, new_word)

    # /rs/ > /ss/ in some words
    # SPECULATION: It's unspecified exactly which environments this occurs in,
    # but from what I can tell, it appears to be blocked by a preceding /o/.
    # Additionally, it looks like /rs/ still occurs in modern plurals as well as
    # some contractions and words which were borrowed at later stages in the
    # language's development.
    new_word = re.sub(r"(?<!o)rs", r"ss", new_word)
    printif(showsteps, new_word)

    # final /-er/, /-or/ > /-re/, /-ro/
    # SPECULATION: It's unspecified whether this also happened to /-ɛr/ and
    # /-ɔr/. Due to the rare occurrence of final, stressed syllables in Latin,
    # it's difficult to find examples. I decided to include them for now.
    new_word = re.sub(r"(!?[eoɛɔ])r$", r"r\1", new_word)
    printif(showsteps, new_word)

    # loss of unstressed internal vowels between /k/, /g/ and /r/, /l/
    new_word = re.sub(r"([bdfgjklmnprstvwz!]*[aeiouɛɔ][kg])[aeiouɛɔ]([rl][!aeiouɛɔ])", r"\1\2", new_word)
    printif(showsteps, new_word)

    # reduction of /e/ and /i/ in hiatus to /j/, followed by palatalization;
    # palatalization of /k/, /g/ before front vowels; /kj/ > /kkj/ prior to
    # palatalization; /dʲ/, /gʲ/ > /j/
    # SPECULATION: It's unclear whether this happened with /ɛ/ or not. I will
    # assume here that it does. It also appears the following <qu> or <gu>, it
    # doesn't palatalize, but remains /j/.
    # NOTE: Later, /j/ stemming from /dʲ/, /gʲ/ undergoes different changes from
    # regular /j/. As such, I indicate such /j/'s using <J>.
    new_word = re.sub(r"(!?)[eiɛ](?=[aeiouɛɔ!])", r"j\1", new_word)
    new_word = re.sub(r"(?<=[bdfgjklmnprstvwz])j", r"ʲ", new_word)
    new_word = re.sub(r"(?<!^)(?<!k)kʲ", r"kkʲ", new_word)
    new_word = re.sub(r"([gk])(?=!?[eiɛ])", r"\1ʲ", new_word)
    new_word = re.sub(r"[dg]ʲ", r"J", new_word)
    printif(showsteps, new_word)

    return new_word



def to_proto_gallo_ibero_romance(word, showprev=True, showsteps=False):

    new_word = to_proto_western_romance(word, showprev)
    if showprev:
        print(new_word, end=" ")

    # /kʲ/, /tʲ/ > /tsʲ/
    new_word = re.sub(r"kkʲ", r"ttsʲ", new_word)
    new_word = re.sub(r"[kt]ʲ", r"tsʲ", new_word)
    printif(showsteps, new_word)

    # /kt/, /ks/ > /jt/, /js/
    new_word = re.sub(r"k(?=[ts])", r"j", new_word)
    printif(showsteps, new_word)

    # first diphthongization: /ɛ/, /ɔ/ > /jɛ/, /wɔ/ in stressed, open syllables
    # and syllables closed by /j/ or /r/ + C
    # SPECULATION: Even though words ending in a consonant should be considered
    # closed, this apparently doesn't apply to words ending in /m/ or /n/, at
    # least in the case of /ɛ/ > /jɛ/. I'm not sure about /ɔ/ > /wɔ/ as I
    # haven't seen any cases of single syllable Latin words (or really any
    # words, for that matter) ending in <om>. It also seems to happen to at
    # least /ɛ/ in syllables closed by /r/, though it doesn't appear to be
    # universal. I'm not sure whether it's more common to do so or not, so for
    # now, I'll assume it's more of an exception than the norm.
    new_word = re.sub(r"!ɛ(?=j|[bdfgGjJkKlmnprstvwz]?ʲ?[aeiouɛɔ]|[nm]$)(?![bdfgGkKlprstvwz]$)", r"j!ɛ", new_word)
    new_word = re.sub(r"!ɔ(?=j|[bdfgGjJkKlmnprstvwz]?ʲ?[aeiouɛɔ])(?![bdfgGkKlmnprstvwz]$)", r"w!ɔ", new_word)
    printif(showsteps, new_word)

    # first unstressed vowel loss: syncope of all post-tonic vowels and syncope
    # of all pre-tonic vowels except /a/, which reduces to schwa in open
    # syllables and remains /a/ in closed syllables
    # SPECULATION: I'm not sure how unstressed diphthongs are affected. For now,
    # I'm sort of handwavingly assuming they might not exist in unstressed
    # syllables anyway, and thus I don't need to worry about it. Additionally, I
    # suspect that there are many instances where simplification of resulting
    # consonant cluster may result. I have found one definitive example
    # (/mn/ > /mm/), but I don't doubt that there are many more. Feel free to
    # include them here if you find any others.
    # NOTE: The standard for central French was for lenition before vowel loss.
    # However, in some dialects it was the opposite. Personally, I prefer the
    # sound of voiceless consonants. As such, I have chosen to implement vowel
    # loss first. If you prefer it the other way, feel free to move this
    # forward. Also, Wikipedia only mentions pre-tonic syncope except /a/. The
    # additional details come from "The Interaction of Vowel Deletion and
    # Syllable Structure Contraints" by Moira Taylor. In her paper, she also
    # mentions that syncope of vowels following C + L combinations typically
    # become a schwa. As much as I struggled with trying to implement a similar
    # feature for apocope during the Early Old French stage, I didn't attempt to
    # implement this aspect of the sound change. If you can get the other one
    # working, feel free to copy it over to here. For now, I think it's easier
    # to just insert a schwa manually if it needs one.
    # pre-tonic syncope
    new_word = re.sub(r"([aeiouɛɔ][bdfgGjJkKlmnprstvwzðɣɲʎʲ]*)[eiouɛɔ](?=[bdfgGjJkKlmnprstvwzðɣɲʎʲ]*![aeiouɛɔ])", r"\1", new_word)
    new_word = re.sub(r"([aeiouɛɔ][bdfgGjJkKlmnprstvwzðɣɲʎʲ]*)a(?=[bdfgGjJkKlmnprstvwzðɣɲʎʲ]![aeiouɛɔ])", r"\1ǝ", new_word)
    # post-tonic syncope
    new_word = re.sub(r"(![aeiouɛɔ][bdfgGjJkKlmnprstvwzðɣɲʎʲ]*)[aeiouɛɔ](?=[bdfgGjJkKlmnprstvwzðɣɲʎʲ]*[aeiouɛɔ])", r"\1", new_word)
    new_word = re.sub(r"mn", r"mm", new_word)
    printif(showsteps, new_word)

    # first lenition: intervocalic voiced stops, unvoiced fricatives > voiced
    # fricatives and unvoiced stops > voiced stops; lenition before /r/
    # following a vowel; /pl/ > /bl/; /kl/, /gl/ > /j/; /gn/ > /jn/; final /t/,
    # /d/ lenited following a vowel
    # SPECULATION: Wikipedia claims that /g/ simply becomes /j/, but there are
    # certain changes in the table of vowel outcomes that involve /ɣ/. It
    # additionally states that /g/ > /j/ when preceded by /a/, e/, /i/ and
    # succeeded by /a/. I suspect /ɣ/ is the more general change, with /j/ only
    # occurring in the aforementioned environment. I'm unsure exactly how /g/
    # lenits before /r/, however, but based on some examples, it appears to
    # become /j/. Thus, I have implemented it as such. Wikipedia also doesn't
    # specify whether this change affects palatalized consonants. I assume here
    # that it does. Regarding diphthongs, it appears that a preceding V + /j/
    # prevents lenition, but not V + /w/. I'm unsure about following diphthongs.
    # For now, I'll assume that it still occurs with following diphthongs.
    new_word = re.sub(r"(?<=[aeiouɛɔǝw])[bf](?=r?ʲ?[aeiouɛɔǝjw!])", r"v", new_word)
    new_word = re.sub(r"(?<=[aeiouɛɔǝw])p(?=[lr]?ʲ?[aeiouɛɔǝjw!])", r"b", new_word)
    new_word = re.sub(r"(?<=[aeiouɛɔǝw])d(?=r?ʲ?[aeiouɛɔǝjw!]|$)", r"ð", new_word)
    new_word = re.sub(r"(?<=[aeiouɛɔǝw])t(?=r?ʲ?[aeiouɛɔǝjw!]|$)", r"d", new_word)
    new_word = re.sub(r"(?<=[aeiouɛɔǝw])s(?=ʲ?[aeiouɛɔǝjw!])", r"z", new_word)
    new_word = re.sub(r"(?<=[aeiouɛɔǝw])g(?=[aeiouɛɔǝjw!])", r"ɣ", new_word)
    new_word = re.sub(r"(?<=[aeiouɛɔǝw])g(?=[rln])", r"j", new_word)
    new_word = re.sub(r"(?<=[aeiǝ])ɣ(?=!?[aǝ])", r"j", new_word)
    new_word = re.sub(r"(?<=[aeiouɛɔǝw])k(?=r?ʲ?[aeiouɛɔǝjw!])", r"g", new_word)
    new_word = re.sub(r"(?<=[aeiouɛɔǝw])K(?=r?ʲ?[aeiouɛɔǝjw!])", r"G", new_word)
    new_word = re.sub(r"k(?=l)", r"j", new_word)
    new_word = re.sub(r"(?<=[aeiouɛɔǝw])tsʲ(?=[aeiouɛɔǝjw!])", r"dzʲ", new_word)
    printif(showsteps, new_word)

    # /jn/, /nj/ > /ɲ/; /jl/ > /ʎ/
    # SPECULATION: Though unspecified, based on some examples, it appears this
    # also happend to /nʲ/ and /lʲ/. I also assume doubled /nn/ and /ll/ become
    # /ɲɲ/ and /ʎʎ/ in palatal contexts as well.
    new_word = re.sub(r"jn|n[jJʲ]", r"ɲ", new_word)
    new_word = re.sub(r"nɲ", r"ɲɲ", new_word)
    new_word = re.sub(r"jl|lʲ", r"ʎ", new_word)
    new_word = re.sub(r"lʎ", r"ʎʎ", new_word)
    printif(showsteps, new_word)

    return new_word



def to_early_old_french(word, showprev=True, showsteps=False):

    new_word = to_proto_gallo_ibero_romance(word, showprev)
    if showprev:
        print(new_word, end=" ")

    # initial /j/ and /j/ when following a consonant and which stems from /dj/,
    # /gj/, or /g(e,i)/> /dʒ/
    # SPECULATION: I don't believe this happened to EVERY /j/ following a
    # consonant as some weird clusters would arise, such as /sdʒ/. In fact,
    # based on analysis of several words in Modern French which contain a /ʒ/
    # following a consonant, it looks like it only occurs after /r/, sometimes
    # /n/ (though typically not), and in cases where it developed from an
    # initial /j/ in the root + a prefix. It's possible these are the only
    # environments this ever occurred in regardless, but I chose to implement it
    # as such anyway.
    # NOTE: At this point, <J> is no longer needed, so I'm replacing it with <j>
    # to simplify things. Additionally, the initial /h/'s that I left in place
    # earlier may now be removed.
    new_word = re.sub(r"^[jJ]|(?<=r)J", r"dʒ", new_word)
    new_word = re.sub(r"J", r"j", new_word)
    new_word = re.sub(r"h", r"", new_word)
    printif(showsteps, new_word)

    # /j/ followed by a consonant palatalizes that consonant
    # SPECULATION: It's not specified if palatalization passes through a series
    # of consonants. For example, would /jtr/ > /jtʲr/, /jtrʲ/, or maybe even
    # /jtʲrʲ/? I'm not sure how frequently, if ever, this sort of thing
    # occurred. However, a later sound change causes certain palatalized
    # consonants to lose their palatal quality and eject a /j/ into the
    # following syllable in certain environments, and based on examples, it
    # appears that this does pass through other consonants. As such, I'm
    # implementing it so that the palatalization passes all the way through (ie,
    # /jtrʲ/). Because it is later lost anyway, it may not even make a
    # difference in the final outcome.
    new_word = re.sub(r"j(?!!)([bdfgklmnprstvzðɣɲʎʒ]+)", r"j\1ʲ", new_word)
    printif(showsteps, new_word)

    # internal palatalized labial become palatal affricates
    new_word = re.sub(r"(?<!^)pʲ", r"tʃ", new_word)
    new_word = re.sub(r"(?<!^)[bv]ʲ", r"dʒ", new_word)
    new_word = re.sub(r"(?<!^)mʲ", r"ndʒ", new_word)
    printif(showsteps, new_word)

    # with the exception of /ɲ/ and /ʎ/, palatalized sounds lose their palatal
    # quality and eject a /j/ into the end of the preceding syllable if open,
    # and also into the beginning of the following syllable if stressed, open
    # /a/ or /e/
    # SPECULATION: /tʃ/, /dʒ/, /ts/, /dz/, /ss/ appear to behave as a single
    # sound when determining open vs closed syllables

    # /tʃ/, /dʒ/ eject a following /j/ but not a preceding /j/
    new_word = re.sub(r"(?<=tʃ|dʒ)(![ae])(?=([bdfgklmnprstvzðɣɲʎ]ʲ?|tʃ|dʒ|tsʲ|dzʲ|ssʲ)?[jw]?[aeiouɛɔǝ]|$)", r"j\1", new_word)
    # when /r/ ejects a preceding /j/, it metathesizes when /a/ precedes
    new_word = re.sub(r"(!?)([aǝ])rʲ(?=[jw]?!?[aeiouɛɔǝ])", r"j\1\2rʲ", new_word)
    # all other consonants
    new_word = re.sub(r"(?<=[aeiouɛɔǝ])([dfgkstzðɣ]ʲ|tsʲ|dzʲ|ssʲ)(?=[jw]?!?[aeiouɛɔǝ])", r"j\1", new_word)
    new_word = re.sub(r"(?<=ʲ)(![ae])(?=([bdfgklmnprstvzðɣɲʎ]ʲ?|tʃ|dʒ|tsʲ|dzʲ|ssʲ)?[aeiouɛɔǝ]|$)", r"j\1", new_word)
    new_word = re.sub(r"ʲ", r"", new_word)
    printif(showsteps, new_word)

    # palatalization of /ka/, /ga/ > /tʃa/, /dʒa/
    # SPECULATION: According to Wikipedia, this step didn't happen until later,
    # but I suspect it had to've happened prior to the second diphthongization,
    # with the exception of the /a/, /e/, /i/ + /k/, /g/ + /a/ > /j/ rule
    # NOTE: <K> and <G> are no longer needed at this point, so I replaced them
    # with <k> and <g> to simplify things going forward.
    new_word = re.sub(r"(?<![aeiǝ])k(?=!?a)", r"tʃ", new_word)
    new_word = re.sub(r"(?<![aeiǝ])g(?=!?a)", r"dʒ", new_word)
    new_word = re.sub(r"K", r"k", new_word)
    new_word = re.sub(r"G", r"g", new_word)
    printif(showsteps, new_word)

    # second diphthongization: stressed open /e/, /o/, /a/ > /ej/, /ow/, /æ/
    # when not followed by /j/
    # SPECULATION: According to the table of vowel outcomes, /a/ > /ɔ/ at some
    # point if followed by /w/, /ɣu/, or /ɣo/. I don't apply this change until
    # later, but I must include a check for it here. Additionally, it appears a
    # following /ɲ/ is apparently considered closed for some reason. Not sure if
    # it applies to /ʎ/ as well, but I'll assume for now that it doesn't.
    new_word = re.sub(r"!e(?!j)(?=([bdfgklmnprstvzðɣʎ]|tʃ|dʒ|ts|dz)?[jw]?[aeiouɛɔǝ]|$)", r"!ej", new_word)
    new_word = re.sub(r"!o(?!j)(?=([bdfgklmnprstvzðɣʎ]|tʃ|dʒ|ts|dz)?[jw]?[aeiouɛɔǝ]|$)", r"!ow", new_word)
    new_word = re.sub(r"!a(?![jw]|ɣ[uo])(?=([bdfgklmnprstvzðɣʎ]|tʃ|dʒ|ts|dz)?[jw]?[aeiouɛɔǝ]|$)", r"!æ", new_word)
    printif(showsteps, new_word)

    # /aw/ > /ɔ/
    # SPECULATION: In the table of vowel outcomes on the Wikipedia page, it
    # indicates that /aw/ + /w/, /ɣu/, or /ɣo/ > /ɔw/ at some point in the Old
    # French stage, but not exactly when. I suspect it occurred here. This
    # change also seemed to happen to plain /a/. Additionally, this change is
    # indicated to have occurred later, but I suspect it had to've happened
    # prior to the second vowel loss, other wise the /o/ or /u/ could be lost,
    # which would lead to different changes. As such, I have moved it back.
    # However, this change must somehow simultaneously occur after the second
    # lention, but the second lention must occur after the second vowel loss, so
    # there's a weird contradiction here. Thus, I have incorporated lenition of
    # /g/ here so the change may be applied correctly prior to the second vowel
    # loss. I am unsure if this affected <gu>. I assume here that it did not.
    # Futhermore, it seems to become /o/ before /j/.
    new_word = re.sub(r"aw?[gɣ](!?)[ou]", r"\1ɔw", new_word)
    new_word = re.sub(r"a(?=w!?[aeiouɛɔæǝ])", r"ɔ", new_word)
    new_word = re.sub(r"aw(?=j)", r"o", new_word)
    new_word = re.sub(r"aw", r"ɔ", new_word)
    printif(showsteps, new_word)

    # second unstressed vowel loss: apocope of all vowels vowels except /a/; a
    # schwa may be inserted to support illegal consonant clusters
    # SPECULATION: It doesn't specifically mention whether this also affects
    # single syllable words or not, but based on some examples, it looks like it
    # doesn't, so I'm implementing it as such. Additionally, even though it says
    # it doesn't affect /a/, I believe that's only partly true. It appears that
    # /a/ becomes schwa. According to wikipedia, this only happens to final /a/
    # and it happens later, but evidence suggests otherwise, so I'm moving it
    # back. Also, as with the first vowel loss, I'm not sure what happens to
    # diphthongs. This time I assume they are lost along with the vowel. Again,
    # it's possible that diphthongs only exist in stressed syllables anyway and
    # this may be a non-issue.
    new_word = re.sub(r"([aeiouɛɔæǝ][jw]?[bdfgklmnprstvzðɣɲʎʃʒ]*)[jw]?[eiouɛɔæǝ][jw]?(?=[bdfgklmnprstvzðɣɲʎʃʒ]*$)", r"\1", new_word)
    new_word = re.sub(r"([aeiouɛɔæǝ][jw]?[bdfgklmnprstvzðɣɲʎʃʒ]*)a(?=[bdfgklmnprstvzðɣɲʎʃʒ]*$)", r"\1ǝ", new_word)
    new_word = re.sub(r"a$", r"ǝ", new_word)

    # NOTE: I experimented here a little with trying to implement a check for
    # whether or not an impermissible final consonant cluster resulted after
    # apocope or not by utilizing the sonority index table described by Moira
    # Taylor, but it ended up causing more harm than good. It might be possible
    # to develop this further, but due to the high complexity of possible
    # consonant clusters that can result, I think it would be easier to just
    # manually add a schwa to the end if you think it needs one. If you're
    # feeling brave, though, feel free to try to accomplish what I couldn't.
##    sonority = {"r" : 7,
##                "l" : 6, "ʎ" : 6,
##                "m" : 5, "n": 5, "ɲ" : 5,
##                "s" : 4,
##                "v" : 3, "z" : 3, "ð" : 3,
##                "f" : 2,
##                "d" : 1, "b" : 1, "g" : 1,
##                "p" : 0.5, "t" : 0.5, "k" : 0.5}
##    vowels = ["e", "i", "o", "u", "ɛ", "ɔ", "æ", "ǝ", "j", "w"]
##    if new_word[-1] not in vowels and new_word[-2] not in vowels and new_word[-1] != new_word[-2]:
##        if sonority[new_word[-2]] - sonority[new_word[-1]] <= 1:
##            if not (((new_word[-1] == "s" or new_word[-1] == "ʃ") and new_word[-2] == "t") or ((new_word[-1] == "z" or new_word[-1] == "ʒ") and new_word[-2] == "d")):
##                new_word += "ǝ"

    printif(showsteps, new_word)

    # second lenition: same as first
    # SPECULATION: Though unspecified, I suspect that /tʃ/ would lenit to /dʒ/
    # as well. Also, as mentioned in the first lenition, /g/ likely developed
    # into /j/ in some environments and /ɣ/ in others. It appears to become /j/
    # between /a/, /e/, /i/, and /a/. I speculate that it also happend with /æ/
    # on either side, as this developed from /a/.
    new_word = re.sub(r"(?<=[aeiouɛɔæǝw])[bf](?=r?[aeiouɛɔæǝjw!])", r"v", new_word)
    new_word = re.sub(r"(?<=[aeiouɛɔæǝw])p(?=[lr]?[aeiouɛɔæǝjw!])", r"b", new_word)
    new_word = re.sub(r"(?<=[aeiouɛɔæǝw])d(?=r?[aeiouɛɔæǝjw!]|$)", r"ð", new_word)
    new_word = re.sub(r"(?<=[aeiouɛɔæǝw])t(?=r?[aeiouɛɔæǝjw!]|$)", r"d", new_word)
    new_word = re.sub(r"(?<=[aeiouɛɔæǝw])s(?=[aeiouɛɔæǝjw!])", r"z", new_word)
    new_word = re.sub(r"(?<=[aeiouɛɔæǝw])g(?=[aeiouɛɔæǝjw!])", r"ɣ", new_word)
    new_word = re.sub(r"(?<=[aeiouɛɔæǝw])g(?=[rln])", r"j", new_word)
    new_word = re.sub(r"(?<=[aeiæǝ])ɣ(?=!?[aæǝ])", r"j", new_word)
    new_word = re.sub(r"(?<=[aeiouɛɔæǝw])k(?=r?[aeiouɛɔæǝjw!])", r"g", new_word)
    new_word = re.sub(r"k(?=l)", r"j", new_word)
    new_word = re.sub(r"(?<=[aeiouɛɔæǝw])ts(?=[aeiouɛɔæǝjw!])", r"dz", new_word)
    new_word = re.sub(r"(?<=[aeiouɛɔæǝw])tʃ(?=[aeiouɛɔæǝjw!])", r"dʒ", new_word)
    printif(showsteps, new_word)

    # /æ/ > /ɛ/ (/jɛ/ after palatals and /aj/ before nasals and not following a
    # palatal)
    # SPECULATION: It's unspecified what constitutes a palatal, but I suspect it
    # includes /tʃ/, /dʒ/.
    new_word = re.sub(r"(?<=tʃ|dʒ)(!?)æ", r"j\1ɛ", new_word)
    new_word = re.sub(r"æ(?=[nm])", r"aj", new_word)
    new_word = re.sub(r"æ", r"ɛ", new_word)
    printif(showsteps, new_word)

    # loss of gemination
    # SPECULATION: To my knowledge, modern French lacks geminated consonants
    # entirely. However, Wikipedia says it only happened to stops, but doesn't
    # indicate when it happened to all other consonants. I'm going to assume it
    # actually all happened at the same time until I find differently.
    new_word = re.sub(r"(.)\1", r"\1", new_word)
    printif(showsteps, new_word)

    # final stops and fricatives lose voicing
    # SPECULATION: It's likely that this also applied to affricates.
    # Additionally, I suspect that any remaining /ɣ/ developed into /j/ by this
    # point.
    new_word = re.sub(r"ɣ", r"j", new_word)
    new_word = re.sub(r"b$", r"p", new_word)
    new_word = re.sub(r"v$", r"f", new_word)
    new_word = re.sub(r"d$", r"t", new_word)
    new_word = re.sub(r"ð$", r"θ", new_word)
    new_word = re.sub(r"z$", r"s", new_word)
    new_word = re.sub(r"g$", r"k", new_word)
    new_word = re.sub(r"dz$", r"ts", new_word)
    new_word = re.sub(r"dʒ$", r"tʃ", new_word)
    printif(showsteps, new_word)

    # /dz/ > /z/ unless final
    new_word = re.sub(r"dz(?!$)", r"z", new_word)
    printif(showsteps, new_word)

    # /t/ inserted between /ɲ/, /ʎ/ and /s/
    new_word = re.sub(r"(?<=[ɲʎ])s", r"ts", new_word)
    printif(showsteps, new_word)

    # /ɲ/, /ʎ/ depalatalized to /jn/, /l/ when final or following a consonant
    # NOTE: Wikipedia contradicts itself by saying saying /ɲ/ depalatalizes to
    # both /n/ and /jn/, but it looks like /jn/ is the correct one based on
    # evidence.
    new_word = re.sub(r"ɲ(?![aeiouɛɔǝ!])|ɲ$", r"jn", new_word)
    new_word = re.sub(r"ʎ(?![aeiouɛɔǝ!])|ʎ$", r"l", new_word)
    printif(showsteps, new_word)

    # /jej/, /wɔj/ > /i/, /uj/
    # SPECULATION: According to the table of vowel outcomes, /jaj/ and /jɛj/
    # also become /i/.
    new_word = re.sub(r"j(!?)[aeɛ]j", r"\1i", new_word)
    new_word = re.sub(r"w(!?)ɔj", r"\1uj", new_word)
    printif(showsteps, new_word)

    return new_word



def to_old_french(word, showprev=True, showsteps=False):

    new_word = to_early_old_french(word, showprev)
    if showprev:
        print(new_word, end=" ")

    # loss of /f/, /p/, /k/ before final /s/, /t/
    new_word = re.sub(r"[fpk](?=[st]$)", r"", new_word)
    printif(showsteps, new_word)

    # nasalization of /a/, /e/, /o/ before /n/, /m/, /ɲ/ (indicated here by a
    # following <ñ> because diacritics don't work very well in this font)
    # SPECULATION: It's doesn't specifically mention nasalization of /ɛ/ and
    # /ɔ/, but based on future changes, I assume they become nasalized here as
    # well. It also doesn't mention nasalization before /ɲ/, but evidence
    # suggests that it occurred in this environment as well.
    new_word = re.sub(r"([aeoɛɔ]w?j?)(?=[nmɲ])", r"\1ñ", new_word)
    printif(showsteps, new_word)

    # /ej/ > /oj/ (blocked by nasalization)
    new_word = re.sub(r"ej(?!ñ)", r"oj", new_word)
    printif(showsteps, new_word)

    # /ow/ > /ew/ (blocked by labials and nasals)
    # SPECULATION: /f/, /v/ don't appear to be considered labials in this
    # context. Wikipedia also doesn't mention that it's blocked by nasalization,
    # but the table in the Late Old French stage seems to indicate that it is.
    new_word = re.sub(r"ow(?![bpmñ])", r"ew", new_word)
    printif(showsteps, new_word)

    # /wɔ/ > /wɛ/ (blocked by nasalization)
    new_word = re.sub(r"w(!?)ɔ(?!ñ)", r"w\1ɛ", new_word)
    printif(showsteps, new_word)

    # /a/ > /ɑ/ before /s/
    new_word = re.sub(r"a(?=s)", r"ɑ", new_word)
    printif(showsteps, new_word)

    # loss of /θ/ and /ð/; resulting /a/ in hiatus becomes schwa
    new_word = re.sub(r"[θð]", r"", new_word)
    new_word = re.sub(r"a(?=!?[aeiouɛɔɑ])", r"ǝ", new_word)
    printif(showsteps, new_word)

    # /s/ > /h/ before consonants
    # SPECULATION: Wikipedia claims this only happened before voiced consonants,
    # but it appears it actually happened before all consonants
    new_word = re.sub(r"s(?!!?[aeiouɛɔɑǝwj]|$)", r"h", new_word)
    printif(showsteps, new_word)

    # /u/ > /y/
    new_word = re.sub(r"u", r"y", new_word)
    printif(showsteps, new_word)

    # nasal /wɔ/ > /u/
    # SPECULATION: It's mentioned in a the Late Old French stage that nasal /wɔ/
    # became nasal /u/, but it doesn't specify exactly when. It had to've
    # happened after the /u/ > /y/ shift because it doesn't develop into nasal
    # /y/. As such, I assume it happened around here.
    new_word = re.sub(r"w(!?)ɔ(?=ñ)", r"\1u", new_word)

    # final /rn/, /rm/ > /r/
    new_word = re.sub(r"r[nm]$", r"r", new_word)
    printif(showsteps, new_word)

    # nasalization of /i/, /u/, /y/ before /n/, /m/, /ɲ/
    # SPECULATION: Again, /ɲ/ isn't mentioned, but it appears to be true.
    new_word = re.sub(r"([uiy]w?j?)(?=[nmɲ])", r"\1ñ", new_word)
    printif(showsteps, new_word)

    return new_word



def to_late_old_french(word, showprev=True, showsteps=False):

    new_word = to_old_french(word, showprev)
    if showprev:
        print(new_word, end=" ")

    # /l/ > /w/ before consonants (except /la/)
    # SPECULATION: It looks like preceding /ɛ/ > /ɛa/ when this change occurs
    # except when preceded by /j/. Also, the /w/ (or it could be the /l/ if it
    # technically occurred before this change) is lost after /i/ or /y/.
    new_word = re.sub(r"(?<![jw])(?<![jw]!)ɛl(?!!?[aeiouyɛɔɑǝwj]|l!?[aɑǝ])", r"ɛal", new_word)
    new_word = re.sub(r"il(?!!?[aeiouyɛɔɑǝwj]|l!?[aɑǝ])", r"i", new_word)
    new_word = re.sub(r"yl(?!!?[aeiouyɛɔɑǝwj]|l!?[aɑǝ])", r"y", new_word)
    new_word = re.sub(r"l(?!!?[aeiouyɛɔɑǝwj]|l!?[aɑǝ])", r"w", new_word)
    printif(showsteps, new_word)

    # /o/ > /u/
    # SPECULATION: Wikipedia says this occurred before the previous change, but
    # because it also happened to /ow/ stemming from /ol/ + C, it must've
    # actually happened later.
    new_word = re.sub(r"ow?(?!j)", r"u", new_word)
    printif(showsteps, new_word)

    # /wɛ/, /ew/ > /œ/
    new_word = re.sub(r"w(!?)ɛ(?!w)", r"\1œ", new_word)
    new_word = re.sub(r"ew", r"œ", new_word)
    printif(showsteps, new_word)

    # /ɔ/ > /o/ before /s/, /œ/ > /ø/ before /s/, /t/
    # SPECULATION: According to the table of vowel outcomes, this change
    # occurred at some point during the Late Old French period, but it's not
    # specified when. I'll insert it here, but It looks like it also happened
    # before /h/, which stemmed from /s/, so I'll account for that.
    new_word = re.sub(r"ɔ(?=[sh])", r"o", new_word)
    new_word = re.sub(r"œ(?=[sht])", r"ø", new_word)

    # falling diphthongs become rising diphthongs
    new_word = re.sub(r"(!?)uj", r"w\1i", new_word)
    new_word = re.sub(r"(!?)yj", r"ɥ\1i", new_word)
    printif(showsteps, new_word)

    # /oj/, /ɔj/ > /wɛ/
    # SPECULATION: Although /ɔj/ > /wɛ/ is not specifically mentioned, I suspect
    # it is the case.
    new_word = re.sub(r"(!?)[oɔ]j", r"w\1ɛ", new_word)
    printif(showsteps, new_word)

    # /aj/ > /ɛ/
    # NOTE: I indicate this with <E> because it resists changes which affect
    # other /ɛ/'s
    new_word = re.sub(r"aj", r"E", new_word)
    printif(showsteps, new_word)

    # /e/ > /ɛ/ in closed syllables
    # SPECULATION: Again, /ɲ/ is considered closed for some reason.
    new_word = re.sub(r"e(?=ñ?ɲ|ñ?[bdfghklmnprstvzɲʎʃʒ]+$|ñ?[bdfghklmnprstvzɲʎʃʒ]{2,})", r"ɛ", new_word)
    printif(showsteps, new_word)

    # /ts/ > /s/, /tʃ/ > /ʃ/, /dʒ/ > /ʒ/
    # SPECULATION: It's unlceare what happened to /dz/, but I assume it
    # deaffricated as well. Additionally, at some point between Old French and
    # Modern French, following /j/ gets absorbed by /ʃ/ and /ʒ/ in some cases.
    # Specifically, it looks like it gets absorbed as long is the following
    # vowel isn't nasal. I'll assume this happens here. Additionally, it appears
    # that the sequence /dtʃ/, which may occur due to the first vowel loss,
    # tends to become /ʒ/ as well.
    new_word = re.sub(r"ts", r"s", new_word)
    new_word = re.sub(r"dz", r"z", new_word)
    new_word = re.sub(r"dtʃ", r"ʒ", new_word)
    new_word = re.sub(r"tʃ", r"ʃ", new_word)
    new_word = re.sub(r"ʃj(?!!?[aeiouyɛEɔɑǝœ]ñ)", r"ʃ", new_word)
    new_word = re.sub(r"ʒj(?!!?[aeiouyɛEɔɑǝœ]ñ)", r"ʒ", new_word)
    new_word = re.sub(r"dʒ", r"ʒ", new_word)
    printif(showsteps, new_word)

    # loss of /h/
    new_word = re.sub(r"h", r"", new_word)
    printif(showsteps, new_word)

    return new_word



def to_middle_french(word, showprev=True, showsteps=False):


    new_word = to_late_old_french(word, showprev)
    if showprev:
        print(new_word, end=" ")

    # /aw/ > /o/, /ɛaw/ > /o/, /ɛw/ > /œ/, /ɔw/ > /u/, /wɛw/ > /œ/, /ow/ > /u/
    # (these mostly result from V + /l/ + C)
    # SPECULATION: Wikipedia only mentions the /aw/ > /o/ change, but I suspect
    # the other vowels were affected around the same time.
    new_word = re.sub(r"ɛaw", r"o", new_word)
    new_word = re.sub(r"aw", r"o", new_word)
    new_word = re.sub(r"w(!?)ɛw", r"\1œ", new_word)
    new_word = re.sub(r"ɛw", r"œ", new_word)
    new_word = re.sub(r"ɔw", r"u", new_word)
    new_word = re.sub(r"ow", r"u", new_word)
    printif(showsteps, new_word)

    # lowering of nasal /u/ > /ɔ/
    # SPECULATION: Wikipedia claims this happened after denasalization, but
    # evidence suggests that it must've happened before in order for nasal /u/
    # to become nonnasal /ɔ/ after denasalization.
    new_word = re.sub(r"u(?=ñ)", r"ɔ", new_word)
    printif(showsteps, new_word)

    # denasalization of vowels when following /n/, /m/, /ɲ/ is followed by
    # another vowel
    # SPECULATION: As above, /ɲ/ is not mentioned, but it appears to follow the
    # same rules as the other nasals.
    new_word = re.sub(r"ñ(?=[nmɲ]!?[aeiouyɛEɔɑœǝwj])", r"", new_word)
    printif(showsteps, new_word)

    # nasal /e/, /ɛ/ > /ɑ/ exept when preceded by /j/ or /w/
    # SPECULATION: Wikipedia claims this happened in the Old French stage, but
    # unlike lowering of nasal /u/ > /ɔ/, which had to occur before
    # denasalization, I suspect it had to've happened after the denasalization
    # step in order to prevent this change in environments which inevitably
    # became denasalized.
    new_word = re.sub(r"(?<![jw])![eɛ](?=ñ)", r"!ɑ", new_word)
    new_word = re.sub(r"(?<![jw]|!)[eɛ](?=ñ)", r"ɑ", new_word)

    # /ej/ > /ɛ/
    new_word = re.sub(r"ej", r"ɛ", new_word)
    printif(showsteps, new_word)

    # deletion of /n/, /m/, /ɲ/ after remaining nasal vowels
    # SPECULATION: Same story regarding /ɲ/.
    new_word = re.sub(r"(?<=ñ)[nmɲ]", r"", new_word)
    printif(showsteps, new_word)

    return new_word



def to_early_modern_french(word, showprev=True, showsteps=False):

    new_word = to_middle_french(word, showprev)
    if showprev:
        print(new_word, end=" ")

    # /wɛ/ > /wa/ (blocked by nasalization)
    # SPECULATION: It may also occasionally become /ɛ/, but it's unclear exactly
    # when then happens, so I ignored this possible change. If you prefer it, go
    # for it. Also, Wikipedia doesn't specifically indicate that it's blocked by
    # nasalization, but it appears to be the case based on the table of vowel
    # outcomes.
    new_word = re.sub(r"w(!?)ɛ(?!ñ)", r"w\1a", new_word)
    printif(showsteps, new_word)

    # loss of final consonants
    # SPECULATION: According to the rules of french orthography, final <f>, <c>,
    # and <l> are usually pronounced. Additionally, final <r> is usually
    # pronounced except after an <e> in words with two or more syllables. As
    # such, I have reflected this here. Note, however, that this is not a hard
    # and fast rule, and that there are MANY exceptions.
    new_word = re.sub(r"[^aeiouyɛEɔɑœǝwjfklrñ]+$", r"", new_word)
    new_word = re.sub(r"([aeiouyɛEɔɑœǝ]ñ?[bdfgjklmnprstvwzɲʎʃʒ]*!?[eɛE])r$", r"\1", new_word)
    printif(showsteps, new_word)

    return new_word



def to_modern_french(word, showprev=True, showsteps=False):

    new_word = to_early_modern_french(word, showprev)
    if showprev:
        print(new_word, end=" ")

    # /r/ > /ʁ/
    new_word = re.sub(r"r", r"ʁ", new_word)
    printif(showsteps, new_word)

    # /ʎ/ > /j/
    new_word = re.sub(r"ʎ", r"j", new_word)
    printif(showsteps, new_word)

    # loss of final schwa
    new_word = re.sub(r"ǝ$", r"", new_word)
    printif(showsteps, new_word)

    # nasal /i/, /y/ > /ɛ/
    new_word = re.sub(r"[iy](?=ñ)", r"ɛ", new_word)
    printif(showsteps, new_word)

    # nasal /a/ > /ɑ/
    new_word = re.sub(r"a(?=ñ)", r"ɑ", new_word)
    printif(showsteps, new_word)

    # merge of nonnasal /ɑ/ and /a/ to /a/
    new_word = re.sub(r"ɑ(?!ñ)", r"a", new_word)
    printif(showsteps, new_word)

    # /ǝ/ > /ø/
    new_word = re.sub(r"ǝ", r"ø", new_word)
    printif(showsteps, new_word)

    # merge of /ɛ/ and /e/ to /e/ (except /ɛ/ stemming from /aj/), merge of /ɔ/
    # and /o/ to /o/, /œ/ > /ø/ when final
    # NOTE: I replace remaining <E>'s with /ɛ/ to simplify because it's no
    # longer needed.
    new_word = re.sub(r"ɛ$", r"e", new_word)
    new_word = re.sub(r"ɔ$", r"o", new_word)
    new_word = re.sub(r"œ$", r"ø", new_word)
    new_word = re.sub(r"E", r"ɛ", new_word)
    printif(showsteps, new_word)

    if showprev:
        print(new_word)

    return new_word



def run_tests():
    tests = [("p!artem", "p!aʁ"),
             ("b!assum", "b!a"),
             ("m!are", "m!ɛʁ"),
             # officially /ɛme/ due to regularization
             ("am!a:tum", "am!e"),
             ("f!agum", "f!u"),
             ("b!auan", "b!u"),
             ("mediet!a:tem", "mwatj!e"),
             ("c!a:rum", "ʃ!ɛʁ"),
             # officially /sɛt/; no idea why final /t/ remains
             ("s!eptem", "s!e"),
             ("h!eri", "j!ɛʁ"),
             ("p!edem", "pj!e"),
             ("s!iccum", "s!ɛk"),
             ("p!e:ram", "pw!aʁ"),
             # officially /vwaʁ/; the /e/ apparently became a schwa, then
             # eventually disappeared; I'm not sure why, as it's unspecified,
             # but if I had to venture a guess: it's due to it being in hiatus
             # with the following vowel
             ("vid!e:re", "vew!aʁ"),
             ("c!e:ram", "s!iʁ"),
             ("merc!e:dem", "mɛʁs!i"),
             ("v!i:tam", "v!i"),
             ("v!i:llam", "v!il"),
             ("p!ortam", "p!ɔʁt"),
             ("s!ottum", "s!o"),
             ("s!ottam", "s!ɔt"),
             ("gr!ossum", "gʁ!o"),
             ("gr!ossam", "gʁ!os"),
             ("n!ovum", "n!œf"),
             ("c!orem", "k!œʁ"),
             ("s!ubtus", "s!u"),
             ("s!urdum", "s!uʁ"),
             ("n!o:dum", "n!ø"),
             ("d!u:rum", "d!yʁ"),
             ("d!u:llam", "d!yl"),
             ("!aurum", "!ɔʁ"),
             ("c!ausam", "ʃ!ɔz"),
             ("tr!aucon", "tʁ!u"),
             ("!annum", "!ɑñ"),
             ("c!antum", "ʃ!ɑñ"),
             ("s!a:nam", "s!ɛn"),
             ("!amat", "!ɛm"),
             ("s!a:num", "s!ɛñ"),
             ("f!amem", "f!ɛñ"),
             ("c!anem", "ʃj!ɛñ"),
             # officially /tjɛn/; I suspect the final /nnt/ resulting from the
             # loss of /e/ might play a part in why there's a final /n/
             ("t!enent", "tj!ɛñ"),
             ("b!ene", "bj!ɛñ"),
             ("t!enet", "tj!ɛñ"),
             ("l!ingua", "l!ɑñg"),
             ("p!e:nam", "p!ɛn"),
             ("pl!e:num", "pl!ɛñ"),
             ("s!inum", "s!ɛñ"),
             ("rac!e:mum", "ʁɛz!ɛñ"),
             ("c!i:nque", "s!ɛñk"),
             ("f!i:num", "f!ɛñ"),
             ("f!i:nam", "f!in"),
             ("p!ontem", "p!ɔñ"),
             ("b!onam", "b!ɔn"),
             ("b!onum", "b!ɔñ"),
             ("c!omes", "k!ɔñ"),
             ("d!o:num", "d!ɔñ"),
             ("d!o:nat", "d!ɔn"),
             ("!u:num", "!ɛñ"),
             # officially /paʁf!ɛñ/; no idea where that /a/ came from
             ("perf!u:mum", "pɛʁf!ɛñ"),
             ("!u:nam", "!yn"),
             ("pl!u:mam", "pl!ym"),
             ("f!estam", "f!ɛt"),
             ("b!e:sta", "b!ɛt"),
             # officially /abim/; I think this might've been borrowed at a later
             # stage in the language, sometime in the Early Old French period
             # after the second vowel loss but before the second lenition, which
             # would explain why the /b/ isn't lenited, but the final /u/ is
             # lost; not sure why the final /m/ remained though
             ("ab!y:smum", "av!i"),
             ("c!ostam", "k!ot"),
             ("c!o:nstat", "k!ut"),
             ("f!u:stis", "f!y"),
             ("f!alsum", "f!o"),
             ("p!almam", "p!om"),
             ("b!ellum", "b!o"),
             ("m!elius", "mj!ø"),
             # officially /ʃǝvø/; it's unclear why the /a/ became schwa
             ("cap!illum", "ʃav!ø"),
             ("f!iltrum", "f!øtʁ"),
             ("gent!i:lem", "ʒɑñt!i"),
             ("f!ollem", "f!u"),
             ("c!olpum", "k!u"),
             ("v!olet", "v!ø"),
             ("p!ulsat", "p!us"),
             ("c!u:lum", "k!y"),
             ("f!actum", "f!ɛ"),
             ("pal!a:tium", "pal!ɛ"),
             ("pl!a:gam", "pl!ɛ"),
             ("pl!acet", "pl!ɛ"),
             # officially /pɛʁ/; it looks like the change in the Early Old
             # French period in which /j/ metathesizes through /a/ upon
             # depalatalization of /r/ wasn't always consistent; perhaps there's
             # actually an unspecified environment which determines the outcome?
             ("p!aria", "pj!ɛʁ"),
             ("!iacet", "ʒ!i"),
             ("c!acat", "ʃ!i"),
             ("l!ectum", "l!i"),
             # officially /sis/; I don't know what it is about numbers and
             # retaining their final consonants, but apparently that's a thing
             ("s!ex", "s!i"),
             ("p!eior", "p!iʁ"),
             ("t!e:ctum", "tw!a"),
             ("r!e:gem", "ʁw!a"),
             ("n!igrum", "nw!aʁ"),
             ("f!e:riam", "fw!aʁ"),
             ("n!octem", "nɥ!i"),
             ("h!odie", "ɥ!i"),
             ("c!oxam", "kɥ!is"),
             ("b!uxitam", "bw!at"),
             ("cr!ucem", "kʁw!a"),
             ("fr!u:ctum", "fʁɥ!i"),
             ("g!audia", "ʒw!a"),
             ("b!aneum", "b!ɛñ"),
             ("s!anctum", "s!ɛñ"),
             ("mont!a:neam", "mɔñt!aɲ"),
             ("p!inctum", "p!ɛñ"),
             # officially /ɑñsɛɲ/; I'm not sure why /ns/ didn't become /s/
             # during the Proto-Western-Romance stage; perhaps is was borrowed in a later stage
             ("ins!igniam", "ez!ɛɲ"),
             ("l!i:neam", "l!iɲ"),
             ("l!onge", "lw!ɛñ"),
             ("fr!ogna", "fʁ!ɔɲ"),
             ("p!unctum", "pw!ɛñ"),
             ("c!uneum", "kw!ɛñ"),
             # officially /vɛʁgɔɲ/; this is a case of the first lenition
             # occurring before the first vowel loss
             ("verec!undiam", "vɛʁk!ɔɲ"),
             ("i!u:nium", "ʒɥ!ɛñ"),
             # officially /epin/; I'm unsure why the /e/ didn't become /ɛ/ in
             # the closed syllable as expected
             ("sp!i:nam", "ɛp!in"),
             ("r!em", "ʁj!ɛñ"),
             ("d!orsum", "d!o"),
             ("!ursum", "!uʁ"),
             ("qu!attuor", "k!atʁ"),
             ("l!i:ber", "l!ivʁ"),
             # officially /tjɛʁ/; this is one of those weird cases where /ɛ/
             # became /jɛ/ even though it was closed
             ("t!ertium", "t!ɛʁ"),
             ("m!anica", "m!ɑñʃ"),
             # officially /gʁɑñʒ/; this is a case of the first lenition
             # occurring before the first vowel loss
             ("gr!a:nica", "gʁ!ɑñʃ"),
             # officially /ʃaʁʒe/; this is another case of the first lenition
             # occurring before the first vowel loss
             ("carric!a:re", "ʃaʁʃ!e"),
             ("vindic!a:re", "vɑñʒ!e"),
             ("impe:ior!a:re", "ɑñpwaʁj!e"),
             # officially /kɥide/; I have no idea why it become /uj/ instead of
             # /oj/; the /d/ is a result of the first lention occurring before
             # the first vowel loss; I don't know why /je/ reduced to /e/, as it
             # was still present in the Old French period, but was lost by the
             # Modern French period
             ("co:git!a:re", "kwatj!e"),
             ("i!ungit", "ʒw!ɛñ"),
             ("oper!a:rium", "uvʁj!e"),
             ("!iungis", "ʒw!ɛñ"),
             ("f!i:lius", "f!i"),
             ("d!iurnum", "ʒ!uʁ"),
             ("v!ermum", "v!ɛʁ"),
             ("d!ormit", "d!ɔʁ"),
             # officially /fam/; this seems to have lowered the nasal /e/ before
             # denasalization; this isn't universal, however, as there are many
             # cases which show the opposite
             ("f!e:minam", "f!em")]

    passed = True
    for i in tests:
        if to_modern_french(i[0], False, False) != i[1]:
            print(f"failed: {i[0]} > {i[1]}")
            passed = False

    if passed:
        print("all tests passed")

run_tests()