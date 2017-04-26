import re
import unicodedata

RX_WS = re.compile(r'\s+')
RX_NL = re.compile(r'\n')


def normalize_space(v: str, convert_whitespace=True, convert_newlines=True):
    """Normalize space."""
    s = v.strip()
    if convert_newlines:
        s = RX_NL.sub(' ', s)
    if convert_whitespace:
        s = RX_WS.sub(' ', s)
    return ' '.join(s.split())


def normalize_unicode(v: str, target='NFC', check_compatible=True):
    """Normalize Unicode."""
    canonical = unicodedata.normalize(target, v)
    if check_compatible and target == 'NFC':
        compatibility_target = 'NFKC'
        compatible = unicodedata.normalize(compatibility_target, v)
        if canonical != compatible:
            msg = (
                'Unicode normalization may have changed the string "{}" in '
                'an undesireable way. The canonical composition form ({}: '
                '"{}") does not match the compatibility composition form ('
                '{}: "{}"). {} is being used.'
                ''.format(
                    v, target, canonical, compatibility_target, compatible,
                    target))
            raise ValueError(msg)
    return canonical
