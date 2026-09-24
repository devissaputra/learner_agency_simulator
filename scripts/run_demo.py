import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from learner_agency_simulator.core import (
    autonomy_preserving_policy,
    compare_policies,
    confusion_hint_policy,
    disengagement_hint_policy,
    no_support_policy,
    sensitivity_study,
    simulate,
)


PROFILE = {
    "help_seeking_tendency": 0.55,
    "support_acceptance": 0.72,
    "persistence": 0.68,
    "challenge_preference": 0.48,
    "strategy_switching": 0.62,
    "autonomy_preference": 0.70,
}

POLICIES = {
    "no_support": no_support_policy,
    "confusion_hint": confusion_hint_policy,
    "disengagement_hint": disengagement_hint_policy,
    "autonomy_preserving": autonomy_preserving_policy,
}

print("One seeded learner-system trajectory")
trajectory = simulate(
    start="productive_struggle",
    steps=8,
    agency_profile=PROFILE,
    system_policy=autonomy_preserving_policy,
    seed=42,
)
for row in trajectory:
    print(row)

print("\nPolicy stress test: 200 runs x 30 steps")
comparison = compare_policies(
    POLICIES,
    runs=200,
    steps=30,
    agency_profile=PROFILE,
    seed=100,
)
for name, metrics in comparison.items():
    print(
        name,
        {
            "mastery_occupancy": round(metrics["mastery_occupancy"], 3),
            "disengagement_occupancy": round(metrics["disengagement_occupancy"], 3),
            "mastery_reached_fraction": round(metrics["mastery_reached_fraction"], 3),
            "mean_interventions": round(metrics["mean_system_interventions"], 3),
            "mean_support_declined": round(metrics["mean_support_declined"], 3),
        },
    )

print("\nSimulator sensitivity: 120 runs x 25 steps")
sensitivity = sensitivity_study(
    POLICIES,
    runs=120,
    steps=25,
    agency_profile=PROFILE,
    seed=300,
)
for scenario, results in sensitivity.items():
    print("Scenario:", scenario)
    for name, metrics in results.items():
        print(
            " ",
            name,
            {
                "mastery": round(metrics["mastery_occupancy"], 3),
                "disengagement": round(metrics["disengagement_occupancy"], 3),
                "interventions": round(metrics["mean_system_interventions"], 3),
            },
        )

print(
    "\nNote: all states, agency parameters, transition probabilities, and policy "
    "effects are synthetic modeling assumptions. Policy comparisons are stress "
    "tests of the simulator, not evidence about real learners."
)
