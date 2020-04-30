"""Normalize whitespace and Unicode forms in Python 3.

Functions:
normalize_space() -- collapse whitespace and trim
normalize_unicode() -- return specified Unicode normal form
"""

__author__ = 'Tom Elliott'
__copyright__ = 'Copyright ©️ 2017 New York University'
__license__ = 'See LICENSE.txt'
__version__ = '0.3'

import logging
import sys
import unicodedata


def normalize_space(v: str, preserve: list = [], trim: bool = True):
    """Normalize space in a Unicode string.

    Keyword arguments:

     * v: the Unicode string to normalize
     * preserve: a list of Unicode character strings to preserve instead of
                 treating them as whitespace (see tests for examples)
     * trim: if True (default), strips whitespace at beginning and end of
                 string; if False, collapses whitespace at beginning and end
                 according to regular algorithm + preserve settings.

    Returns the normalized Unicode string.

    The function collapses all continuous runs of whitespace into a single
    whitespace character unless one or more characters are found in the
    "preserve" list. Characters found in the "preserve" list are maintained in
    the output; however, other adjoining whitespace characters are still
    eliminated. If "trim" is True, leading/trailing whitespace is eliminated
    entirely, otherwise these is treated the same as other whitespace
    substrings.
    """
    
    logger = logging.getLogger(sys._getframe().f_code.co_name)

    if len(preserve) == 0:
        s = ' '.join(v.split())
    else:
        token = preserve[0]
        normed = []
        for chunk in v.split(token):
            normed.append(normalize_space(chunk, preserve[1:]))
        s = token.join(normed)
    if not trim:
        if v != s:
            first = ''
            last = ''
            chunks = v.split()
            vi = v.index(chunks[0])
            si = s.index(chunks[0])
            if si == 0 and v[0] != s[0]:
                first = ' '
            vi = v.index(chunks[-1]) + len(chunks[-1])
            si = s.index(chunks[-1]) + len(chunks[-1])
            if si == len(s) and len(v) > vi:
                last = ' '
            s = first + s + last
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
