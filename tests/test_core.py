import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from learner_agency_simulator import core


class CoreTests(unittest.TestCase):
    def test_simulation_is_reproducible(self):
        first = core.simulate(steps=5, seed=7)
        second = core.simulate(steps=5, seed=7)
        self.assertEqual(first, second)
        self.assertEqual(len(first), 6)

    def test_transition_returns_known_state(self):
        self.assertIn(core.step("confusion", seed=1), core.STATES)


if __name__ == "__main__":
    unittest.main()
