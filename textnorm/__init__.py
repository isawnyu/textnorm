"""Normalize whitespace and Unicode forms in Python 3.

Functions:
normalize_space() -- collapse whitespace and trim
normalize_unicode() -- return specified Unicode normal form
"""

__author__ = 'Tom Elliott'
__copyright__ = 'Copyright ©️ 2017 New York University'
__license__ = 'See LICENSE.txt'
__version__ = '0.2'


import re
import unicodedata

RX_WS = re.compile(r'\s+')
RX_NL = re.compile(r'\n')


def normalize_space(v: str, convert_whitespace=True, convert_newlines=True):
    """Normalize space in a Unicode string.

    Keyword arguments:

     * v: the Unicode string to normalize
     * convert_whitespace: treat all whitespace characters except newline as
       space
     * convert_newlines: treat newlines as space characters

    Returns the normalized Unicode string.

    The function collapses all continuous runs of whitespace into a single
    whitespace character and leading and trailing spaces are trimmed away.
    If convert_whitespace is True, then each whitespace character other than
    newline is converted to a plain space prior to collapsing. If
    convert_newline is True, then all newline characters are first converted
    to plain spaces prior to collapsing.
    """
    s = v.strip()
    if convert_newlines:
        s = RX_NL.sub(' ', s)
    if convert_whitespace:
        s = RX_WS.sub(' ', s)
    return ' '.join(s.split())


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
