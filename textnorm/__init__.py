"""Normalize whitespace and Unicode forms in Python 3.

Functions:
normalize_space() -- collapse whitespace and trim
normalize_unicode() -- return specified Unicode normal form
"""

__author__ = 'Tom Elliott'
__copyright__ = 'Copyright ©️ 2017 New York University'
__license__ = 'See LICENSE.txt'
__version__ = '0.3'

import re
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
    canonical = unicodedata.normalize(target, v)
    if check_compatible:
        if target == 'NFC':
            compatibility_target = 'NFKC'
        elif target == 'NFD':
            compatibility_target = 'NFKD'
        compatible = unicodedata.normalize(compatibility_target, v)
        if canonical != compatible:
            msg = (
                'Unicode normalization may have changed the string "{}" in '
                'an undesireable way. The canonical composition form ({}: '
                '"{}") does not match the compatibility composition form ('
                '{}: "{}").'
                ''.format(
                    v, target, canonical, compatibility_target, compatible))
            raise ValueError(msg)
    return canonical
