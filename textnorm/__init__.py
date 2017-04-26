"""Normalize whitespace and Unicode forms in Python 3.

Functions:
normalize_space() -- collapse whitespace and trim
normalize_unicode() -- return specified Unicode normal form
"""

__author__ = 'Tom Elliott'
__copyright__ = 'Copyright ©️ 2017 New York University'
__license__ = 'See LICENSE.txt'
__version__ = '0.3'

import unicodedata


def normalize_space(v: str, preserve: list=[]):
    """Normalize space in a Unicode string.

    Keyword arguments:

     * v: the Unicode string to normalize
     * convert_whitespace: treat all whitespace characters except newline as
                           space
     * preserve: a list of Unicode character strings to preserve instead of
                 treating them as whitespace (see tests for examples)

    Returns the normalized Unicode string.

    The function collapses all continuous runs of whitespace into a single
    whitespace character and leading and trailing spaces are trimmed away.
    If one or more characters are found in the "preserve" list, these are
    maintained in the output; however, other adjoining whitespace characters
    are still eliminated.
    """
    if len(preserve) == 0:
        s = ' '.join(v.split())
    else:
        token = preserve[0]
        normed = []
        for chunk in v.split(token):
            normed.append(normalize_space(chunk, preserve[1:]))
        s = token.join(normed)
    return s


def normalize_unicode(v: str, target='NFC', check_compatible=False):
    """Normalize Unicode form.

    Keyword arguments:

     * v: the Unicode string to normalize
     * target: the targeted normalization form as a string expected by
               unicodedata.normalize(). No checking is done on the value of
               this argument.
     * check_compatible: detect differences in canonical and compatibility
                         form results

    Returns the normalized Unicode string.

    Raises ValueError if check_compatible is True and the canonical and
    compatibility forms differ.

    This function wraps unicodedata.normalize from the standard library,
    adding the optional compatibility check when appropriate.
    """
    normalized = unicodedata.normalize(target, v)
    normalized = _sort_diacritics(normalized)
    if check_compatible:
        if target == 'NFC':
            compatibility_target = 'NFKC'
        elif target == 'NFD':
            compatibility_target = 'NFKD'
        elif target == 'NFKC':
            compatibility_target = 'NFC'
        elif target == 'NFKD':
            compatibility_target = 'NFD'
        compatible = unicodedata.normalize(compatibility_target, v)
        if normalized != compatible:
            msg = (
                'Unicode normalization may have changed the string "{}" in '
                'an undesireable way or may have failed to do so in a manner '
                'desired. The {} normalized form '
                '"{}" ({}) does not match the corresponding {} form '
                '"{}" ({}).'
                ''.format(
                    v,
                    target,
                    normalized,
                    normalized.encode('ascii', 'namereplace'),
                    compatibility_target,
                    compatible,
                    compatible.encode('ascii', 'namereplace')))
            raise ValueError(msg)
    return normalized


def _sort_diacritics(v: str):
    """Ensure combining diacritics are always ordered the same way.

    It appears that unicodedata.normalize does not enforce a canonical
    ordering of combining diacritics in NFD and NFKD when the string
    being normalized contains combining diacritics in arbitrary order and
    the 'Canonical Combining Class' of two or more of those diacritics has
    the same value. This function sorts all combining diacriticals that
    follow a character with combining class == 0 first according to their
    combining classes and then according to their code point value. This
    ensures a repeatable sequence, regardless of the arbitrary order in
    which the combining diacritics in the input string occur.
    """

    def postfix(v: list):
        if len(v) > 0:
            return ''.join(
                sorted(
                    v,
                    key=lambda x: (unicodedata.combining(x), ord(x))))
        else:
            return ''

    result = ''
    diacritics = []
    for c in v:
        if unicodedata.combining(c) == 0:
            result += postfix(diacritics)  # diacritics for preceding character
            diacritics = []
            result += c  # now the current non-combining character
        else:
            diacritics.append(c)
    result += postfix(diacritics)  # final diacritics
    return result
