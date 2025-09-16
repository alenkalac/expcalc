from unittest import TestCase

import Utils


class Test(TestCase):

    def test_extract_exp(self):
        expected = "50320579[76.06%]"
        actual = Utils.extract_exp('[3747/3747] P[908/2716] P50320579[76.06%]')

        self.assertEqual(expected, actual)

    def test_calc_time_to_level(self):
        ttl = Utils.calc_time_to_level(0.00, 10)
        self.assertEqual("1h 40m", ttl)

    def test_validate_exp_string(self):
        self.assertTrue(Utils.validate_exp_string("79[76.06%]"))
        self.assertTrue(Utils.validate_exp_string("79[76.06%"))
        self.assertFalse(Utils.validate_exp_string("79[76.06"))
        self.assertFalse(Utils.validate_exp_string("7976.06%"))
        self.assertFalse(Utils.validate_exp_string("79[7606%"))
        self.assertFalse(Utils.validate_exp_string("797606%"))
