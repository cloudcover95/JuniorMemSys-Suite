from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from junior_memsys_suite.lattice.msis_commit import commit, verify


class MsisTests(unittest.TestCase):
    def test_roundtrip(self):
        z = [1, 0, -1, 1] * 8
        c = commit(z)
        self.assertTrue(verify(z, c))
        z2 = list(z)
        z2[0] = -z2[0] if z2[0] else 1
        self.assertFalse(verify(z2, c))


if __name__ == "__main__":
    unittest.main(verbosity=2)
