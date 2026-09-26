# Calculation reading guide: ../CALCULATIONS.md (repository root).
# State occupancy = observations in state / all recorded states.
# The initial state is included in occupancy; transition counts exclude it. Policy differences are consequences of the specified simulator, not estimated effects in real learners. Sensitivity to the transition assumptions is central.

import math
import random
from collections.abc import Callable, Mapping, Sequence
from numbers import Real


STATES = (
    "mastery",
    "productive_struggle",
    "confusion",
    "disengagement",
)

LEARNER_ACTIONS = (
    "continue",
    "request_hint",
    "request_example",
    "change_strategy",
    "choose_easier_task",
    "choose_harder_task",
    "pause",
    "decline_support",
)

SYSTEM_ACTIONS = (
    "none",
    "guided_hint",
    "worked_example",
    "reflection_prompt",
    "challenge",
)

DEFAULT_AGENCY_PROFILE = {
    "help_seeking_tendency": 0.45,
    "support_acceptance": 0.75,
    "persistence": 0.65,
    "challenge_preference": 0.45,
    "strategy_switching": 0.55,
    "autonomy_preference": 0.60,
}

BASE_TRANSITIONS = {
    "mastery": {
        "mastery": 0.68,
        "productive_struggle": 0.22,
        "confusion": 0.06,
        "disengagement": 0.04,
    },
    "productive_struggle": {
        "mastery": 0.26,
        "productive_struggle": 0.46,
        "confusion": 0.20,
        "disengagement": 0.08,
    },
    "confusion": {
        "mastery": 0.08,
        "productive_struggle": 0.28,
        "confusion": 0.46,
        "disengagement": 0.18,
    },
    "disengagement": {
        "mastery": 0.02,
        "productive_struggle": 0.14,
        "confusion": 0.18,
        "disengagement": 0.66,
    },
}


def _validate_probability(value: Real, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(f"{name} must be numeric")
    value = float(value)
    if not math.isfinite(value) or not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be finite and between 0 and 1")
    return value


def validate_transition_matrix(
    matrix: Mapping[str, Mapping[str, Real]],
) -> dict[str, dict[str, float]]:
    if set(matrix) != set(STATES):
        raise ValueError("transition matrix must define every learner state exactly once")

    validated = {}
    for state in STATES:
        row = matrix[state]
        if set(row) != set(STATES):
            raise ValueError(
                f"transition row for {state} must define every learner state"
            )
        values = {
            target: _validate_probability(
                probability,
                f"{state}->{target}",
            )
            for target, probability in row.items()
        }
        if not math.isclose(sum(values.values()), 1.0, abs_tol=1e-9):
            raise ValueError(f"transition probabilities for {state} must sum to 1")
        validated[state] = values
    return validated


def validate_agency_profile(
    profile: Mapping[str, Real] | None = None,
) -> dict[str, float]:
    merged = dict(DEFAULT_AGENCY_PROFILE)
    if profile is not None:
        unknown = set(profile) - set(DEFAULT_AGENCY_PROFILE)
        if unknown:
            raise ValueError(
                f"unknown agency profile fields: {sorted(unknown)}"
            )
        for key, value in profile.items():
            merged[key] = _validate_probability(value, key)
    return merged


def _normalize(weights: Mapping[str, float]) -> dict[str, float]:
    if set(weights) != set(STATES):
        raise ValueError("transition weights must cover every state")
    total = sum(weights.values())
    if total <= 0:
        raise ValueError("transition weights must sum to a positive value")
    return {
        state: max(0.0, weight) / total
        for state, weight in weights.items()
    }


def _shift(
    probabilities: Mapping[str, float],
    changes: Mapping[str, float],
) -> dict[str, float]:
    """Apply bounded additive transition shifts and renormalize."""
    adjusted = {
        state: max(
            0.0,
            probabilities[state] + changes.get(state, 0.0),
        )
        for state in STATES
    }
    return _normalize(adjusted)


def _draw_choice(
    probabilities: Mapping[str, float],
    rng: random.Random,
) -> str:
    draw = rng.random()
    cumulative = 0.0
    last_key = None
    for key, probability in probabilities.items():
        last_key = key
        cumulative += probability
        if draw <= cumulative:
            return key
    return last_key


def learner_action_probabilities(
    state: str,
    profile: Mapping[str, Real] | None = None,
    *,
    support_offer: str = "none",
) -> dict[str, float]:
    if state not in STATES:
        raise ValueError(f"unknown learner state: {state}")
    if support_offer not in SYSTEM_ACTIONS:
        raise ValueError(f"unknown system action: {support_offer}")

    p = validate_agency_profile(profile)

    if state == "mastery":
        weights = {
            "continue": 0.42,
            "request_hint": 0.01,
            "request_example": 0.01,
            "change_strategy": 0.03,
            "choose_easier_task": 0.02,
            "choose_harder_task": 0.30 + 0.35 * p["challenge_preference"],
            "pause": 0.08,
            "decline_support": 0.08 + 0.18 * p["autonomy_preference"],
        }
    elif state == "productive_struggle":
        weights = {
            "continue": 0.25 + 0.35 * p["persistence"],
            "request_hint": 0.08 + 0.28 * p["help_seeking_tendency"],
            "request_example": 0.04 + 0.16 * p["help_seeking_tendency"],
            "change_strategy": 0.06 + 0.28 * p["strategy_switching"],
            "choose_easier_task": 0.06,
            "choose_harder_task": 0.05 + 0.12 * p["challenge_preference"],
            "pause": 0.06,
            "decline_support": 0.06 + 0.15 * p["autonomy_preference"],
        }
    elif state == "confusion":
        weights = {
            "continue": 0.08 + 0.15 * p["persistence"],
            "request_hint": 0.15 + 0.38 * p["help_seeking_tendency"],
            "request_example": 0.12 + 0.30 * p["help_seeking_tendency"],
            "change_strategy": 0.10 + 0.32 * p["strategy_switching"],
            "choose_easier_task": 0.10,
            "choose_harder_task": 0.01 + 0.04 * p["challenge_preference"],
            "pause": 0.09,
            "decline_support": 0.05 + 0.14 * p["autonomy_preference"],
        }
    else:
        weights = {
            "continue": 0.06 + 0.16 * p["persistence"],
            "request_hint": 0.08 + 0.22 * p["help_seeking_tendency"],
            "request_example": 0.05 + 0.18 * p["help_seeking_tendency"],
            "change_strategy": 0.05 + 0.18 * p["strategy_switching"],
            "choose_easier_task": 0.08,
            "choose_harder_task": 0.01,
            "pause": 0.22,
            "decline_support": 0.10 + 0.22 * p["autonomy_preference"],
        }

    if support_offer == "none":
        weights["decline_support"] = 0.0
    else:
        acceptance = p["support_acceptance"]
        weights["decline_support"] += 0.55 * (1.0 - acceptance)
        if support_offer == "guided_hint":
            weights["request_hint"] += 0.35 * acceptance
        elif support_offer == "worked_example":
            weights["request_example"] += 0.35 * acceptance
        elif support_offer == "challenge":
            weights["choose_harder_task"] += (
                0.25 * acceptance * p["challenge_preference"]
            )
        elif support_offer == "reflection_prompt":
            weights["change_strategy"] += (
                0.22 * acceptance * p["strategy_switching"]
            )

    total = sum(weights.values())
    return {
        action: weight / total
        for action, weight in weights.items()
    }


def choose_learner_action(
    state: str,
    profile: Mapping[str, Real] | None = None,
    *,
    support_offer: str = "none",
    rng: random.Random | None = None,
    seed: int | None = None,
) -> str:
    if rng is not None and seed is not None:
        raise ValueError("provide rng or seed, not both")
    rng = rng or random.Random(seed)
    probabilities = learner_action_probabilities(
        state,
        profile,
        support_offer=support_offer,
    )
    return _draw_choice(probabilities, rng)


def resolve_support(
    system_action: str,
    learner_action: str,
) -> str:
    if system_action not in SYSTEM_ACTIONS:
        raise ValueError(f"unknown system action: {system_action}")
    if learner_action not in LEARNER_ACTIONS:
        raise ValueError(f"unknown learner action: {learner_action}")

    if learner_action == "decline_support":
        return "none"
    if learner_action == "request_hint":
        return "guided_hint"
    if learner_action == "request_example":
        return "worked_example"
    return system_action


def transition_probabilities(
    state: str,
    learner_action: str = "continue",
    system_action: str = "none",
    *,
    matrix: Mapping[str, Mapping[str, Real]] | None = None,
) -> dict[str, float]:
    if state not in STATES:
        raise ValueError(f"unknown learner state: {state}")
    if learner_action not in LEARNER_ACTIONS:
        raise ValueError(f"unknown learner action: {learner_action}")
    if system_action not in SYSTEM_ACTIONS:
        raise ValueError(f"unknown system action: {system_action}")

    matrix = validate_transition_matrix(matrix or BASE_TRANSITIONS)
    probabilities = matrix[state]

    learner_adjustments = {
        "continue": {},
        "request_hint": {
            "productive_struggle": 0.10,
            "confusion": -0.07,
            "disengagement": -0.03,
        },
        "request_example": {
            "mastery": 0.05,
            "productive_struggle": 0.08,
            "confusion": -0.09,
            "disengagement": -0.04,
        },
        "change_strategy": {
            "productive_struggle": 0.12,
            "confusion": -0.08,
            "disengagement": -0.04,
        },
        "choose_easier_task": {
            "mastery": 0.05,
            "productive_struggle": 0.08,
            "confusion": -0.08,
            "disengagement": -0.05,
        },
        "choose_harder_task": {
            "mastery": -0.05,
            "productive_struggle": 0.11,
            "confusion": 0.04,
            "disengagement": -0.10,
        },
        "pause": {
            "productive_struggle": -0.02,
            "confusion": -0.03,
            "disengagement": 0.05,
        },
        "decline_support": {},
    }

    system_adjustments = {
        "none": {},
        "guided_hint": {
            "mastery": 0.04,
            "productive_struggle": 0.10,
            "confusion": -0.09,
            "disengagement": -0.05,
        },
        "worked_example": {
            "mastery": 0.07,
            "productive_struggle": 0.08,
            "confusion": -0.10,
            "disengagement": -0.05,
        },
        "reflection_prompt": {
            "mastery": 0.02,
            "productive_struggle": 0.12,
            "confusion": -0.08,
            "disengagement": -0.06,
        },
        "challenge": {
            "mastery": -0.07,
            "productive_struggle": 0.14,
            "confusion": 0.05,
            "disengagement": -0.12,
        },
    }

    adjusted = _shift(
        probabilities,
        learner_adjustments[learner_action],
    )
    adjusted = _shift(
        adjusted,
        system_adjustments[system_action],
    )
    return adjusted


def _validate_steps(steps: int) -> int:
    if isinstance(steps, bool) or not isinstance(steps, int):
        raise ValueError("steps must be an integer")
    if steps < 0:
        raise ValueError("steps must be non-negative")
    return steps


def step(
    state: str,
    *,
    learner_action: str = "continue",
    system_action: str = "none",
    matrix: Mapping[str, Mapping[str, Real]] | None = None,
    seed: int | None = None,
) -> str:
    probabilities = transition_probabilities(
        state,
        learner_action,
        system_action,
        matrix=matrix,
    )
    return _draw_choice(probabilities, random.Random(seed))


def no_support_policy(state: str, history: Sequence[dict]) -> str:
    return "none"


def confusion_hint_policy(state: str, history: Sequence[dict]) -> str:
    return "guided_hint" if state == "confusion" else "none"


def disengagement_hint_policy(state: str, history: Sequence[dict]) -> str:
    return "guided_hint" if state == "disengagement" else "none"


def autonomy_preserving_policy(state: str, history: Sequence[dict]) -> str:
    if state == "disengagement":
        return "reflection_prompt"
    return "none"


def simulate(
    start: str = "productive_struggle",
    steps: int = 20,
    *,
    agency_profile: Mapping[str, Real] | None = None,
    system_policy: Callable[[str, Sequence[dict]], str] | None = None,
    matrix: Mapping[str, Mapping[str, Real]] | None = None,
    seed: int = 42,
) -> list[dict]:
    """Simulate learner choices, system offers, resolved support, and state transitions."""
    _validate_steps(steps)
    if start not in STATES:
        raise ValueError(f"unknown learner state: {start}")
    profile = validate_agency_profile(agency_profile)
    transition_matrix = validate_transition_matrix(matrix or BASE_TRANSITIONS)
    policy = system_policy or no_support_policy

    rng = random.Random(seed)
    state = start
    history = [
        {
            "step": 0,
            "state": state,
            "learner_action": None,
            "system_offer": None,
            "resolved_support": None,
            "next_state": state,
        }
    ]

    for index in range(1, steps + 1):
        system_offer = policy(state, tuple(history))
        if system_offer not in SYSTEM_ACTIONS:
            raise ValueError(
                f"system policy returned unknown action: {system_offer}"
            )
        learner_action = choose_learner_action(
            state,
            profile,
            support_offer=system_offer,
            rng=rng,
        )
        resolved_support = resolve_support(
            system_offer,
            learner_action,
        )
        probabilities = transition_probabilities(
            state,
            learner_action,
            resolved_support,
            matrix=transition_matrix,
        )
        next_state = _draw_choice(probabilities, rng)
        history.append(
            {
                "step": index,
                "state": state,
                "learner_action": learner_action,
                "system_offer": system_offer,
                "resolved_support": resolved_support,
                "next_state": next_state,
            }
        )
        state = next_state

    return history


def trajectory_metrics(history: Sequence[Mapping[str, object]]) -> dict:
    if not history:
        raise ValueError("history must not be empty")

    states = [row["next_state"] for row in history]
    transition_rows = list(history[1:])
    denominator = max(1, len(states))

    interventions = [
        row
        for row in transition_rows
        if row["system_offer"] != "none"
    ]
    accepted = [
        row
        for row in interventions
        if row["resolved_support"] != "none"
    ]
    declined = [
        row
        for row in interventions
        if row["resolved_support"] == "none"
    ]
    requested = [
        row
        for row in transition_rows
        if row["learner_action"] in ("request_hint", "request_example")
    ]

    disengaged_transitions = [
        row
        for row in transition_rows
        if row["state"] == "disengagement"
    ]
    recovered = [
        row
        for row in disengaged_transitions
        if row["next_state"] != "disengagement"
    ]

    first_mastery = next(
        (
            index
            for index, state in enumerate(states)
            if state == "mastery"
        ),
        None,
    )

    return {
        "steps": len(transition_rows),
        "mastery_occupancy": states.count("mastery") / denominator,
        "productive_struggle_occupancy": states.count("productive_struggle") / denominator,
        "confusion_occupancy": states.count("confusion") / denominator,
        "disengagement_occupancy": states.count("disengagement") / denominator,
        "time_to_first_mastery": first_mastery,
        "system_interventions": len(interventions),
        "learner_requested_support": len(requested),
        "support_accepted": len(accepted),
        "support_declined": len(declined),
        "disengagement_recovery_rate": (
            len(recovered) / len(disengaged_transitions)
            if disengaged_transitions
            else None
        ),
    }


def evaluate_policy(
    policy: Callable[[str, Sequence[dict]], str],
    *,
    runs: int = 200,
    steps: int = 30,
    start: str = "productive_struggle",
    agency_profile: Mapping[str, Real] | None = None,
    matrix: Mapping[str, Mapping[str, Real]] | None = None,
    seed: int = 42,
) -> dict:
    if isinstance(runs, bool) or not isinstance(runs, int) or runs <= 0:
        raise ValueError("runs must be a positive integer")
    _validate_steps(steps)

    metrics = []
    for offset in range(runs):
        history = simulate(
            start,
            steps,
            agency_profile=agency_profile,
            system_policy=policy,
            matrix=matrix,
            seed=seed + offset,
        )
        metrics.append(trajectory_metrics(history))

    def mean(name: str) -> float:
        values = [
            row[name]
            for row in metrics
            if row[name] is not None
        ]
        return sum(values) / len(values) if values else float("nan")

    mastered = [
        row["time_to_first_mastery"]
        for row in metrics
        if row["time_to_first_mastery"] is not None
    ]

    return {
        "runs": runs,
        "steps": steps,
        "mastery_occupancy": mean("mastery_occupancy"),
        "productive_struggle_occupancy": mean("productive_struggle_occupancy"),
        "confusion_occupancy": mean("confusion_occupancy"),
        "disengagement_occupancy": mean("disengagement_occupancy"),
        "mastery_reached_fraction": len(mastered) / runs,
        "mean_time_to_first_mastery": (
            sum(mastered) / len(mastered)
            if mastered
            else None
        ),
        "mean_system_interventions": mean("system_interventions"),
        "mean_learner_requested_support": mean("learner_requested_support"),
        "mean_support_accepted": mean("support_accepted"),
        "mean_support_declined": mean("support_declined"),
        "mean_disengagement_recovery_rate": mean("disengagement_recovery_rate"),
    }


def compare_policies(
    policies: Mapping[str, Callable[[str, Sequence[dict]], str]],
    **kwargs,
) -> dict:
    if not isinstance(policies, Mapping) or not policies:
        raise ValueError("policies must be a non-empty mapping")
    results = {}
    for name, policy in policies.items():
        if not isinstance(name, str) or not name.strip():
            raise ValueError("policy names must be non-empty strings")
        results[name] = evaluate_policy(policy, **kwargs)
    return results


def perturb_transition_matrix(
    matrix: Mapping[str, Mapping[str, Real]] | None = None,
    *,
    disengagement_persistence_delta: float = 0.0,
    confusion_persistence_delta: float = 0.0,
) -> dict[str, dict[str, float]]:
    base = validate_transition_matrix(matrix or BASE_TRANSITIONS)

    for value, name in (
        (disengagement_persistence_delta, "disengagement_persistence_delta"),
        (confusion_persistence_delta, "confusion_persistence_delta"),
    ):
        if isinstance(value, bool) or not isinstance(value, Real):
            raise ValueError(f"{name} must be numeric")
        if not math.isfinite(float(value)):
            raise ValueError(f"{name} must be finite")

    updated = {
        state: dict(row)
        for state, row in base.items()
    }

    def shift_persistence(state: str, delta: float) -> None:
        if math.isclose(delta, 0.0, abs_tol=1e-15):
            return
        current = updated[state][state]
        target = current + float(delta)
        if not 0.0 <= target <= 0.95:
            raise ValueError(
                f"{state} persistence adjustment is outside the supported range"
            )
        difference = target - current
        other_states = [
            candidate
            for candidate in STATES
            if candidate != state
        ]
        available = sum(updated[state][candidate] for candidate in other_states)
        if available <= 0:
            raise ValueError("cannot redistribute transition probability")
        for candidate in other_states:
            share = updated[state][candidate] / available
            updated[state][candidate] -= difference * share
        updated[state][state] = target

    shift_persistence(
        "disengagement",
        float(disengagement_persistence_delta),
    )
    shift_persistence(
        "confusion",
        float(confusion_persistence_delta),
    )
    return validate_transition_matrix(updated)


def sensitivity_study(
    policies: Mapping[str, Callable[[str, Sequence[dict]], str]],
    *,
    scenarios: Mapping[str, Mapping[str, float]] | None = None,
    runs: int = 200,
    steps: int = 30,
    agency_profile: Mapping[str, Real] | None = None,
    seed: int = 42,
) -> dict:
    scenarios = scenarios or {
        "baseline": {},
        "sticky_disengagement": {
            "disengagement_persistence_delta": 0.10,
        },
        "sticky_confusion": {
            "confusion_persistence_delta": 0.10,
        },
        "more_recoverable": {
            "disengagement_persistence_delta": -0.10,
            "confusion_persistence_delta": -0.08,
        },
    }

    results = {}
    for scenario_name, changes in scenarios.items():
        matrix = perturb_transition_matrix(
            BASE_TRANSITIONS,
            **changes,
        )
        results[scenario_name] = compare_policies(
            policies,
            runs=runs,
            steps=steps,
            agency_profile=agency_profile,
            matrix=matrix,
            seed=seed,
        )
    return results
