from unittest import TestCase

from old.Payload import Payload


class TestPayload(TestCase):
    def test_read_byte(self):
        p = Payload("0102")
        b1 = p.read_byte()
        self.assertEqual("01", b1)

        b2 = p.read_byte()
        self.assertEqual("02", b2)

    def test_read_byte_throws_error(self):
        p = Payload("0102")
        with self.assertRaises(ValueError):
            p.skip(6)
