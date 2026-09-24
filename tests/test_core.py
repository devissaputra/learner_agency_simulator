import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from learner_agency_simulator import core


class CoreTests(unittest.TestCase):
    def test_transition_matrix_is_valid(self):
        matrix = core.validate_transition_matrix(core.BASE_TRANSITIONS)
        self.assertEqual(set(matrix), set(core.STATES))
        for row in matrix.values():
            self.assertAlmostEqual(sum(row.values()), 1.0)

    def test_invalid_transition_row_sum_is_rejected(self):
        matrix = {
            state: dict(row)
            for state, row in core.BASE_TRANSITIONS.items()
        }
        matrix["mastery"]["mastery"] = 0.9
        with self.assertRaises(ValueError):
            core.validate_transition_matrix(matrix)

    def test_distinct_states_have_distinct_dynamics(self):
        self.assertNotEqual(
            core.BASE_TRANSITIONS["mastery"],
            core.BASE_TRANSITIONS["productive_struggle"],
        )
        self.assertNotEqual(
            core.BASE_TRANSITIONS["productive_struggle"],
            core.BASE_TRANSITIONS["confusion"],
        )

    def test_default_profile_validates(self):
        profile = core.validate_agency_profile()
        self.assertEqual(
            set(profile),
            set(core.DEFAULT_AGENCY_PROFILE),
        )

    def test_profile_rejects_unknown_field(self):
        with self.assertRaises(ValueError):
            core.validate_agency_profile({"mystery": 0.5})

    def test_profile_rejects_invalid_probability(self):
        with self.assertRaises(ValueError):
            core.validate_agency_profile({"persistence": 1.5})

    def test_action_probabilities_sum_to_one(self):
        probabilities = core.learner_action_probabilities("confusion")
        self.assertAlmostEqual(sum(probabilities.values()), 1.0)

    def test_confusion_increases_help_seeking_options(self):
        confusion = core.learner_action_probabilities("confusion")
        mastery = core.learner_action_probabilities("mastery")
        self.assertGreater(
            confusion["request_hint"],
            mastery["request_hint"],
        )

    def test_support_offer_changes_action_distribution(self):
        none = core.learner_action_probabilities(
            "confusion",
            support_offer="none",
        )
        hint = core.learner_action_probabilities(
            "confusion",
            support_offer="guided_hint",
        )
        self.assertNotEqual(none, hint)

    def test_learner_action_is_seed_reproducible(self):
        first = core.choose_learner_action("confusion", seed=7)
        second = core.choose_learner_action("confusion", seed=7)
        self.assertEqual(first, second)

    def test_decline_support_resolves_to_none(self):
        self.assertEqual(
            core.resolve_support("guided_hint", "decline_support"),
            "none",
        )

    def test_request_hint_can_override_none_offer(self):
        self.assertEqual(
            core.resolve_support("none", "request_hint"),
            "guided_hint",
        )

    def test_guided_hint_changes_confusion_transition(self):
        baseline = core.transition_probabilities(
            "confusion",
            "continue",
            "none",
        )
        supported = core.transition_probabilities(
            "confusion",
            "request_hint",
            "guided_hint",
        )
        self.assertLess(
            supported["confusion"],
            baseline["confusion"],
        )

    def test_worked_example_changes_help_requested_transition(self):
        baseline = core.transition_probabilities(
            "productive_struggle",
            "continue",
            "none",
        )
        supported = core.transition_probabilities(
            "productive_struggle",
            "request_example",
            "worked_example",
        )
        self.assertGreater(
            supported["mastery"],
            baseline["mastery"],
        )

    def test_step_returns_known_state(self):
        result = core.step(
            "confusion",
            learner_action="request_hint",
            system_action="guided_hint",
            seed=1,
        )
        self.assertIn(result, core.STATES)

    def test_steps_reject_boolean(self):
        with self.assertRaises(ValueError):
            core.simulate(steps=True)

    def test_steps_reject_float(self):
        with self.assertRaises(ValueError):
            core.simulate(steps=3.5)

    def test_simulation_is_reproducible(self):
        first = core.simulate(steps=5, seed=7)
        second = core.simulate(steps=5, seed=7)
        self.assertEqual(first, second)
        self.assertEqual(len(first), 6)

    def test_simulation_records_actions_and_support(self):
        history = core.simulate(
            steps=5,
            system_policy=core.confusion_hint_policy,
            seed=7,
        )
        for row in history[1:]:
            self.assertIn(row["learner_action"], core.LEARNER_ACTIONS)
            self.assertIn(row["system_offer"], core.SYSTEM_ACTIONS)
            self.assertIn(row["resolved_support"], core.SYSTEM_ACTIONS)
            self.assertIn(row["next_state"], core.STATES)

    def test_invalid_policy_action_is_rejected(self):
        def bad_policy(state, history):
            return "magic"

        with self.assertRaises(ValueError):
            core.simulate(steps=1, system_policy=bad_policy)

    def test_trajectory_metrics_have_expected_keys(self):
        history = core.simulate(steps=10, seed=3)
        metrics = core.trajectory_metrics(history)
        self.assertEqual(metrics["steps"], 10)
        self.assertIn("mastery_occupancy", metrics)
        self.assertIn("support_declined", metrics)

    def test_occupancies_are_bounded(self):
        metrics = core.trajectory_metrics(
            core.simulate(steps=20, seed=4)
        )
        for key in (
            "mastery_occupancy",
            "productive_struggle_occupancy",
            "confusion_occupancy",
            "disengagement_occupancy",
        ):
            self.assertGreaterEqual(metrics[key], 0.0)
            self.assertLessEqual(metrics[key], 1.0)

    def test_evaluate_policy_is_reproducible(self):
        first = core.evaluate_policy(
            core.confusion_hint_policy,
            runs=30,
            steps=12,
            seed=11,
        )
        second = core.evaluate_policy(
            core.confusion_hint_policy,
            runs=30,
            steps=12,
            seed=11,
        )
        self.assertEqual(first, second)

    def test_evaluate_policy_rejects_invalid_runs(self):
        with self.assertRaises(ValueError):
            core.evaluate_policy(core.no_support_policy, runs=0)

    def test_compare_policies_returns_all_named_policies(self):
        results = core.compare_policies(
            {
                "none": core.no_support_policy,
                "confusion_hint": core.confusion_hint_policy,
            },
            runs=20,
            steps=10,
        )
        self.assertEqual(
            set(results),
            {"none", "confusion_hint"},
        )

    def test_policy_comparison_produces_intervention_difference(self):
        results = core.compare_policies(
            {
                "none": core.no_support_policy,
                "confusion_hint": core.confusion_hint_policy,
            },
            runs=60,
            steps=15,
            seed=5,
        )
        self.assertGreater(
            results["confusion_hint"]["mean_system_interventions"],
            results["none"]["mean_system_interventions"],
        )

    def test_perturbation_changes_disengagement_persistence(self):
        matrix = core.perturb_transition_matrix(
            disengagement_persistence_delta=0.10,
        )
        self.assertGreater(
            matrix["disengagement"]["disengagement"],
            core.BASE_TRANSITIONS["disengagement"]["disengagement"],
        )
        self.assertAlmostEqual(
            sum(matrix["disengagement"].values()),
            1.0,
        )

    def test_invalid_perturbation_is_rejected(self):
        with self.assertRaises(ValueError):
            core.perturb_transition_matrix(
                disengagement_persistence_delta=1.0,
            )

    def test_sensitivity_study_returns_scenarios(self):
        result = core.sensitivity_study(
            {
                "none": core.no_support_policy,
                "autonomy": core.autonomy_preserving_policy,
            },
            runs=20,
            steps=10,
            seed=9,
        )
        self.assertIn("baseline", result)
        self.assertIn("sticky_disengagement", result)
        self.assertIn("more_recoverable", result)

    def test_support_acceptance_changes_action_distribution(self):
        low = core.learner_action_probabilities(
            "confusion",
            {"support_acceptance": 0.0},
            support_offer="guided_hint",
        )
        high = core.learner_action_probabilities(
            "confusion",
            {"support_acceptance": 1.0},
            support_offer="guided_hint",
        )
        self.assertGreater(
            low["decline_support"],
            high["decline_support"],
        )

    def test_high_help_seeking_changes_request_probability(self):
        low = core.learner_action_probabilities(
            "confusion",
            {"help_seeking_tendency": 0.0},
        )
        high = core.learner_action_probabilities(
            "confusion",
            {"help_seeking_tendency": 1.0},
        )
        self.assertGreater(
            high["request_hint"],
            low["request_hint"],
        )

    def test_metrics_do_not_return_infinite_values(self):
        metrics = core.evaluate_policy(
            core.no_support_policy,
            runs=20,
            steps=10,
        )
        for value in metrics.values():
            if isinstance(value, float):
                self.assertFalse(math.isinf(value))


if __name__ == "__main__":
    unittest.main()
