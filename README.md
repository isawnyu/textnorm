# textnorm

A simple package for normalizing whitespace and Unicode composition forms in Python 3 strings.

The package provides two functions, as follows. Extended use examples may be found in ```tests/tests.py```.

## normalize_space

This function takes a Python 3 string argument (```v```) and returns a Python string in which each continuous sequence of one or more whitespace characters found in ```v``` has been collapsed into a single whitespace character. 

Basic usage is as simple as:

```python
from textnorm import normalize_space
s = ' There        was an\tOld \tMan in a tree,\t\t'
n = normalize_space(s)
print('"{}"'.format(n))
```

which produces output like:

```
"There was an Old Man in a tree,"
```

By default, characters like newlines (```\n```) are treated as any other whitespace character, such that use like this:

```python
s = """I’m now arrived—thanks to the gods!—  
   Thro’ pathways rough and muddy,  
 A certain sign that makin roads  
   Is no this people’s study:  """
print('"{}"'.format(normalize_space(s)))
```

yields a result like this: 

```
"I’m now arrived—thanks to the gods!— Thro’ pathways rough and muddy, A certain sign that makin roads Is no this people’s study:"
```

An optional keyword argument (```preserve```) may be used to designate a list of one or more whitespace characters that are to be left untouched. So, it is possible to preserve the newlines in the string from the preceding example while normalizing the rest of the whitespace:

```python
print('"{}"'.format(normalize_space(s, preserve = ['\n'])))
```

which produces: 

```
"I’m now arrived—thanks to the gods!—
Thro’ pathways rough and muddy,
A certain sign that makin roads
Is no this people’s study:"
```

Another optional keyword argument (```trim```) can be used to adjust handling of whitespace appearing at the beginning and end of the input string. Leading and trailing characters indicated in the ```preserve``` argument are always protected, but otherwise ```trim=True``` (the default) ensures a result with no leading or trailing whitespace. If the input string has leading or trailing whitespace and ```trim``` is set to ```False```, then the result string will have either a single space character corresponding to the original leading/trailing whitespace characters **or** a sequence of preserved whitespace characters copied from the original. For examples:

```python
s = '\t\n orange '
print('"{}"'.format(normalize_space(s, trim=False)))
```

produces

```python
" orange "
```

and 

```python
s = '\t\n orange '
print('"{}"'.format(normalize_space(s, preserve=['\n'], trim=False)))
```

produces 

```python
"
orange "
```

but

```python
s = '\t\n orange '
print('"{}"'.format(normalize_space(s, trim=True)))  # default
```

produces

```python
"orange"
```

## normalize_unicode

The second function wraps ```unicodedata.normalize``` from the standard library, adding some minor additional functionality. Its primary purpose retains that of ```unicodedata.normalize```, i.e., to return the specified normal form ('NFC', 'NFD', 'NFKC', 'NFKD')  for the Unicode string provided to the function. 

Explaining Unicode normalization is beyond the scope of this readme file; however, I can recommend the following for additional reading:

 - [J.K. Tauber's article on "Python, Unicode and Ancient Greek."](https://jktauber.com/articles/python-unicode-ancient-greek/)
 - [_The Python Standard Library_, Section 6.5 "unicodedata — Unicode Database"](https://docs.python.org/3.6/library/unicodedata.html)
 - ["Unicode Equivalence" in _Wikipedia_](https://en.wikipedia.org/wiki/Unicode_equivalence)

Basic usage of ```textnorm.normalize_unicode``` looks like this:

```python
from textnorm import normalize_unicode
s_nfc = 'μ\u03adγα βιβλ\u03afον μ\u03adγα κακ\u03ccν'  # NB: "composed" forms of accented characters 
n_nfd = normalize_unicode(s_nfc, 'NFD')
n_nfc = normalize_unicode(n_nfd, 'NFC')
print(s_nfc == n_nfd)
print(s_nfc == n_nfc)
print('original NFC: "{}"'.format(s_nfc))
print('normalized NFD: "{}"'.format(n_nfd))
print('round-tripped NFC: "{}"'.format(n_nfc))
```

which produces output like this:

```
False
True
original NFC: "μέγα βιβλίον μέγα κακόν"
normalized NFD: "μέγα βιβλίον μέγα κακόν"
round-tripped NFC: "μέγα βιβλίον μέγα κακόν"
```

Even though modern software and fonts are pretty good and making the NFC and NFC forms appear identical, if you examine the underlying encoding you can see that the differences are real. 

### added functionality: compatibility checking

Over and above the functionality provided by unicodedata.normalize, textnorm.normalize_unicode has a ```check_compatible``` argument that, if ```True```, triggers a comparison of the targeted normalization form with the corresponding "compatibility" form (i.e., it compares 'NFC' with 'NFKC' and 'NFD' with 'NFKD'). If the "canonical" and "compatibility" forms differ, the function raises ```ValueError``` with a diagnostic message. A calling program that traps for this exception can then implement double-checking or supervision.

The lunate sigma ('Ϲ' == '\u03f9') provides a good way to demonstrate this behavior since the canonical forms (NFC and NFD) preserve the character, but the "compatibility" forms (NFKC and NFKD) convert it to conventional sigma ('Σ' == '\u03a3'). First, we'll conduct the conversion without a test:

```python
s = '\u03f9υρβανή'  # i.e. Ϲυρβανή
n = normalize_unicode(s, 'NFKC')
print(n)
```

and we get

```
Συρβανή
```

But, if we activate the test: 

```python
s = '\u03f9υρβανή'  # i.e. Ϲυρβανή
n = normalize_unicode(s, 'NFKC', check_compatible=True)
```

we'll be treated to the informative traceback:

```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/paregorios/Documents/files/T/textnorm/textnorm/__init__.py", line 93, in normalize_unicode
    raise ValueError(msg)
ValueError: Unicode normalization may have changed the string "Ϲυρβανή" in an undesireable way or may have failed to do so in a manner desired. The NFKC normalized form "Συρβανή" (b'\\N{GREEK CAPITAL LETTER SIGMA}\\N{GREEK SMALL LETTER UPSILON}\\N{GREEK SMALL LETTER RHO}\\N{GREEK SMALL LETTER BETA}\\N{GREEK SMALL LETTER ALPHA}\\N{GREEK SMALL LETTER NU}\\N{GREEK SMALL LETTER ETA WITH TONOS}') does not match the corresponding NFC form "Ϲυρβανή" (b'\\N{GREEK CAPITAL LUNATE SIGMA SYMBOL}\\N{GREEK SMALL LETTER UPSILON}\\N{GREEK SMALL LETTER RHO}\\N{GREEK SMALL LETTER BETA}\\N{GREEK SMALL LETTER ALPHA}\\N{GREEK SMALL LETTER NU}\\N{GREEK SMALL LETTER ETA WITH TONOS}').
```

## etc

Pull requests and new tickets on the issue tracker are welcome. 

*This README has been created with thanks and apologies to https://www.poets.org and to the ghosts of Robert Burns and Edward Lear.*

