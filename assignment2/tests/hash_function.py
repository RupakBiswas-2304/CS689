import unittest
from hash_function import to_bitstring, hash

class TestHashFunction(unittest.TestCase):
    def test_to_bitstring(self):
        assert(to_bitstring(4) ==  "00000100")