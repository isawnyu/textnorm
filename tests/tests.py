"""Tests for the normtext package."""

__author__ = 'Tom Elliott'
__copyright__ = 'Copyright ©️ 2017 New York University'
__license__ = 'See LICENSE.txt'
__version__ = '0.3'

from nose.tools import assert_equal, assert_not_equal, raises
from textnorm import normalize_space, normalize_unicode
import unittest


class SpaceTests(unittest.TestCase):

    def setUp(self):
        self.goal = 'The quick brown fox jumped over the lazy sea urchin.'

    def tearDown(self):
        pass

    def test_empty(self):
        s = ''
        n = normalize_space(s)
        assert_equal(s, n)

    def test_unity(self):
        s = self.goal
        n = normalize_space(s)
        assert_equal(self.goal, n)

    def test_trim(self):
        s = '  The quick brown fox jumped over the lazy sea urchin. '
        n = normalize_space(s)
        assert_equal(
           'The quick brown fox jumped over the lazy sea urchin.', n)

    def test_trim_false(self):
        s = '  The quick brown fox jumped over the lazy sea urchin. '
        n = normalize_space(s, trim=False)
        assert_equal(
           ' The quick brown fox jumped over the lazy sea urchin. ', n)

    def test_interstitial(self):
        s = '  The quick   brown fox jumped over    the lazy sea urchin. '
        n = normalize_space(s)
        assert_equal(self.goal, n)

    def test_tabs(self):
        s = '\tThe\tquick \t brown fox jumped over    the lazy sea urchin. '
        n = normalize_space(s)
        assert_equal(self.goal, n)

    def test_tabs_preserve(self):
        s = '\tThe\tquick \t brown fox jumped over    the lazy sea urchin. '
        g = '\tThe\tquick\tbrown fox jumped over the lazy sea urchin.'
        n = normalize_space(s, preserve=['\t'])
        assert_equal(g, n)

    def test_newlines(self):
        s = '\nThe\nquick \n brown fox jumped over    the lazy sea urchin. '
        n = normalize_space(s)
        assert_equal(self.goal, n)

    def test_newlines_preserve(self):
        s = '\nThe\nquick \n brown fox jumped over    the lazy sea urchin. '
        g = '\nThe\nquick\nbrown fox jumped over the lazy sea urchin.'
        n = normalize_space(s, preserve=['\n'])
        assert_equal(g, n)

    def test_nonbreaking_space(self):
        s = (
            'The\u00A0quick\u00A0brown\u00A0fox  jumped  over  the lazy sea '
            'urchin.')
        n = normalize_space(s)
        assert_equal(self.goal, n)

    def test_nonbreaking_space_preserve(self):
        s = (
            'The\u00A0quick\u00A0brown\u00A0fox  jumped  over  the lazy sea '
            'urchin.')
        g = (
            'The\u00A0quick\u00A0brown\u00A0fox jumped over the lazy sea '
            'urchin.')
        n = normalize_space(s, preserve=['\u00A0'])
        assert_equal(g, n)

    def test_mixed(self):
        s = (
            '\tThe quick brown\u00A0fox \n \t jumped over\n\t\tthe\nlazy\nsea '
            'urchin.\n\t   \n ')
        n = normalize_space(s)
        assert_equal(self.goal, n)

    def test_mixed_preserve(self):
        s = (
            '\tThe quick brown\u00A0fox \n \t jumped over\n\t\tthe\nlazy\nsea '
            'urchin.\n\t   \n ')
        g = (
            '\tThe quick brown\u00A0fox\n\tjumped over\n\t\tthe\nlazy\nsea '
            'urchin.\n\t\n')
        n = normalize_space(s, preserve=['\t', '\n', '\u00A0'])
        assert_equal(g, n)

        

class UnicodeTests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_empty(self):
        s = ''
        n = normalize_space(s)
        assert_equal(s, n)

    def test_unity_roman(self):
        s = 'Cats rule. Dogs drool.'
        n = normalize_space(s)
        assert_equal(s, n)

    def test_unity_greek(self):
        s = 'μέγα βιβλίον μέγα κακόν'
        n = normalize_unicode(s)
        assert_equal(s, n)

    # Greek starting in NFC

    def test_greek_nfc2nfc(self):
        s = 'μ\u03adγα βιβλ\u03afον μ\u03adγα κακ\u03ccν'
        n = normalize_unicode(s)
        assert_equal(s, n)
        n = normalize_unicode(s, target='NFC')
        assert_equal(s, n)

    def test_greek_nfc2nfd(self):
        s = 'μ\u03adγα βιβλ\u03afον μ\u03adγα κακ\u03ccν'
        n = normalize_unicode(s, target='NFD')
        g = (
            'μ\u03b5\u0301γα βιβλ\u03b9\u0301ον μ\u03b5\u0301γα '
            'κακ\u03bf\u0301ν')
        assert_equal(g, n)

    def test_greek_nfc2nfkc(self):
        s = 'μ\u03adγα βιβλ\u03afον μ\u03adγα κακ\u03ccν'
        n = normalize_unicode(s, target='NFKC')
        assert_equal(s, n)

    def test_greek_nfc2nfkd(self):
        s = 'μ\u03adγα βιβλ\u03afον μ\u03adγα κακ\u03ccν'
        n = normalize_unicode(s, target='NFKD')
        g = (
            'μ\u03b5\u0301γα βιβλ\u03b9\u0301ον μ\u03b5\u0301γα '
            'κακ\u03bf\u0301ν')
        assert_equal(g, n)

    # Greek starting in NFD

    def test_greek_nfd2nfd(self):
        s = (
            'μ\u03b5\u0301γα βιβλ\u03b9\u0301ον μ\u03b5\u0301γα '
            'κακ\u03bf\u0301ν')
        n = normalize_unicode(s, target='NFD')
        assert_equal(s, n)

    def test_greek_nfd2nfc(self):
        s = (
            'μ\u03b5\u0301γα βιβλ\u03b9\u0301ον μ\u03b5\u0301γα '
            'κακ\u03bf\u0301ν')
        n = normalize_unicode(s, target='NFC')
        g = 'μ\u03adγα βιβλ\u03afον μ\u03adγα κακ\u03ccν'
        assert_equal(g, n)

    def test_greek_nfd2nfkc(self):
        s = (
            'μ\u03b5\u0301γα βιβλ\u03b9\u0301ον μ\u03b5\u0301γα '
            'κακ\u03bf\u0301ν')
        n = normalize_unicode(s, target='NFKC')
        g = 'μ\u03adγα βιβλ\u03afον μ\u03adγα κακ\u03ccν'
        assert_equal(g, n)

    def test_greek_nfd2nfkd(self):
        s = (
            'μ\u03b5\u0301γα βιβλ\u03b9\u0301ον μ\u03b5\u0301γα '
            'κακ\u03bf\u0301ν')
        n = normalize_unicode(s, target='NFKD')
        assert_equal(s, n)

    # Greek starting in NFKD

    def test_greek_nfkd2nfkd(self):
        s = (
            'μ\u03b5\u0301γα βιβλ\u03b9\u0301ον μ\u03b5\u0301γα '
            'κακ\u03bf\u0301ν')
        n = normalize_unicode(s, target='NFKD')
        assert_equal(s, n)

    def test_greek_nfkd2nfc(self):
        s = (
            'μ\u03b5\u0301γα βιβλ\u03b9\u0301ον μ\u03b5\u0301γα '
            'κακ\u03bf\u0301ν')
        n = normalize_unicode(s, target='NFC')
        g = 'μ\u03adγα βιβλ\u03afον μ\u03adγα κακ\u03ccν'
        assert_equal(g, n)

    def test_greek_nfkd2nfd(self):
        s = (
            'μ\u03b5\u0301γα βιβλ\u03b9\u0301ον μ\u03b5\u0301γα '
            'κακ\u03bf\u0301ν')
        n = normalize_unicode(s, target='NFD')
        assert_equal(s, n)

    def test_greek_nfkd2nfkc(self):
        s = (
            'μ\u03b5\u0301γα βιβλ\u03b9\u0301ον μ\u03b5\u0301γα '
            'κακ\u03bf\u0301ν')
        n = normalize_unicode(s, target='NFKC')
        g = 'μ\u03adγα βιβλ\u03afον μ\u03adγα κακ\u03ccν'
        assert_equal(g, n)

    # Greek Extended compatibility forms

    def test_greek_extended2nfc(self):
        s = 'μ\u1f73γα βιβλ\u1f77ον μ\u1f73γα κακ\u1f79ν'
        n = normalize_unicode(s, target='NFC')
        g = 'μ\u03adγα βιβλ\u03afον μ\u03adγα κακ\u03ccν'
        assert_equal(g, n)

    def test_greek_extended2nfkc(self):
        s = 'μ\u1f73γα βιβλ\u1f77ον μ\u1f73γα κακ\u1f79ν'
        n = normalize_unicode(s, target='NFKC')
        g = 'μ\u03adγα βιβλ\u03afον μ\u03adγα κακ\u03ccν'
        assert_equal(g, n)

    def test_greek_extended2nfd(self):
        s = 'μ\u1f73γα βιβλ\u1f77ον μ\u1f73γα κακ\u1f79ν'
        n = normalize_unicode(s, target='NFD')
        g = (
            'μ\u03b5\u0301γα βιβλ\u03b9\u0301ον μ\u03b5\u0301γα '
            'κακ\u03bf\u0301ν')
        assert_equal(g, n)

    def test_greek_extended2nfkd(self):
        s = 'μ\u1f73γα βιβλ\u1f77ον μ\u1f73γα κακ\u1f79ν'
        n = normalize_unicode(s, target='NFKD')
        g = (
            'μ\u03b5\u0301γα βιβλ\u03b9\u0301ον μ\u03b5\u0301γα '
            'κακ\u03bf\u0301ν')
        assert_equal(g, n)

    # Greek variant letterforms and compatibility check

    def test_greek_lunate_sigma2nfc(self):
        s = '\u03f9υρβαν\u03ae'
        n = normalize_unicode(s, target='NFC')
        assert_equal(s, n)

    @raises(ValueError)
    def test_greek_lunate_sigma2nfc_compatible(self):
        s = '\u03f9υρβαν\u03ae'
        normalize_unicode(s, target='NFC', check_compatible=True)

    def test_greek_lunate_sigma2nfd(self):
        s = '\u03f9υρβαν\u03ae'
        n = normalize_unicode(s, target='NFD')
        g = '\u03f9υρβαν\u03b7\u0301'
        assert_equal(g, n)

    @raises(ValueError)
    def test_greek_lunate_sigma2nfd_compatible(self):
        s = '\u03f9υρβαν\u03ae'
        normalize_unicode(s, target='NFD', check_compatible=True)

    def test_greek_lunate_sigma2nfkd(self):
        s = '\u03f9υρβαν\u03ae'
        n = normalize_unicode(s, target='NFKD')
        g = '\u03a3υρβαν\u03b7\u0301'
        assert_equal(g, n)

    @raises(ValueError)
    def test_greek_lunate_sigma2nfkd_compatible(self):
        s = '\u03f9υρβαν\u03ae'
        normalize_unicode(s, target='NFKD', check_compatible=True)

    def test_greek_lunate_sigma2nfkc(self):
        s = '\u03f9υρβαν\u03ae'
        n = normalize_unicode(s, target='NFKC')
        g = '\u03a3υρβαν\u03ae'
        assert_equal(g, n)

    @raises(ValueError)
    def test_greek_lunate_sigma2nfkc_compatible(self):
        s = '\u03f9υρβαν\u03ae'
        normalize_unicode(s, target='NFKC', check_compatible=True)

    # multiple combining diacritics

    def test_combining_nfd2nfd(self):
        raise NotImplementedError

    def test_combining_nfd2nfkd(self):
        raise NotImplementedError

    def test_combining_nfd2nfc(self):
        raise NotImplementedError

    def test_combining_nfd2nfkc(self):
        raise NotImplementedError

    def test_combining_heretical2nfd(self):
        raise NotImplementedError

    @raises(ValueError)
    def test_combining_heretical2nfd_compatible(self):
        raise NotImplementedError
