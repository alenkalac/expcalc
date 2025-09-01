from unittest import TestCase

import ExpClac


class Test(TestCase):

    def test_extract_exp(self):
        expected = "50320579[76.06%"
        actual = ExpClac.extract_exp('[3747/3747] P[908/2716] P50320579[76.06%]')

        self.assertEqual(expected, actual)
