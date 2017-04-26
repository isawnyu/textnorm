# textnorm

A simple package for normalizing whitespace and Unicode composition forms in Python 3 strings.

The package provides two functions:

 - normalize_space
 - normalize_unicode

The second function simply wraps [unicodedata](https://docs.python.org/3.6/library/unicodedata.html).normalize, adding an optional test for differences between canonical and compatibility forms.

Pull requests are welcome. 
