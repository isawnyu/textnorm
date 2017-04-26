"""Tests for the normtext package."""

__author__ = 'Tom Elliott'
__copyright__ = 'Copyright ©️ 2017 New York University'
__license__ = 'See LICENSE.txt'
__version__ = '0.3'


from nose.tools import assert_equal
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
