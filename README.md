# French-Converter
A Python script which simulates the sound changes from Latin to French. This was written in 3.11, but should be able to run in any version >=3.6. Don't quote me on that though. It also requires the `regex` module.

## Introduction
The three versions in the main folder are old as dirt and not the most accurate. I'm really only holding onto them because they were some of my first coding projects and they make me feel kind of nostalgic.

The best and most up to date version is in the `new` folder.

Note that this is not a spelling predictor, but a sound predictor. French spelling is heavily influenced by older forms, much like English. However, you can look at the word at the end of the Old French period for a rough estimate.

I should also note that while the final results are fairly accurate (at least for all the cases I tested. I'm sure there are plenty I missed), I would take the intermediate steps with a grain of salt. I tried my best to make sense of the logical inconsistencies of Wikipedia and tried to substitute in external sources where I could, but it's far from perfect. There's also a ton of exceptions that are simply impossible to account for.

One thing I might do in the future is attempt to tackle the reduction of illegal consonant clusters, referring to the possible clusters that may result after vowel loss. There are so many possibilities that I could drive myself mad just trying to account for all of them, so if you run the code and get a result with a really bizarre consonant cluster, that's probably why. For the time being, you'll have to use your best judgment, unfortunately. However, I can point you to two excellent sources to assist in this endeavor, both of which helped me greatly during this project: "From Latin to Modern French" by M. K. Pope (specifically chapter 8), and "Historical Primer of French Phonetics and Inflection" by Margaret S. Brittain (specifically chapters 9-12).

## How to Use
To evolve a word, use the `evolve` function. This takes two arguments: the word to evolve, and an optional Boolean indicating whether or not to print out every single change along the way (the default is `False`). Be warned that if you set the second argument to `True`, you will get punched in the face by 100s of lines of output.

Note that this function will simulate the changes all the way from Latin to Modern French, which didn't apply to all words. Many were borrowed into the language at different stages of its development. As such, there are additional functions for each major stage of the French language that you can use to simulate borrowings in those stages.

Before you can evolve a word, it will need some minimal "setup". Firstly, mark the stressed vowel with a `/` immediately before the vowel, as in `p/artem`. Secondly, to mark long vowels, use a `:`, as in `am/a:tum`. Additonally, a little preprocessing is required:
* Replace any `c`s with `k`.
* Replace any `qu`s with `kw`.
* You may need to replace `gu` with `gw`, but not universally. Use your best judgment.
* Replace any `x`s with `ks`.
* Replace any intervocal (meaning between two vowels) `u`s with `w` and `i`s with `j`.
* Replace the diphthongs `ae` with `aj`, `oe` with `oj`, and `au` with `aw`.

To understand the output, you'll need a good understanding of IPA. If you think I'm referring to the beer, then you're gonna have problems.

If you encounter any issues please let me know and I'll try to correct them.
