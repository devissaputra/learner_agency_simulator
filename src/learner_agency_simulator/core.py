import random

STATES = (
    "mastery",
    "productive_struggle",
    "confusion",
    "disengagement",
    "help_seeking",
)


def _probabilities(state: str, support: str) -> dict[str, float]:
    if state not in STATES:
        raise ValueError(f"unknown learner state: {state}")
    if support not in ("none", "guided_hint"):
        raise ValueError(f"unknown support action: {support}")

    if state == "disengagement":
        if support == "guided_hint":
            return {
                "mastery": 0.05,
                "productive_struggle": 0.30,
                "confusion": 0.20,
                "disengagement": 0.25,
                "help_seeking": 0.20,
            }
        return {
            "mastery": 0.02,
            "productive_struggle": 0.15,
            "confusion": 0.18,
            "disengagement": 0.55,
            "help_seeking": 0.10,
        }
    if state == "confusion":
        return {
            "mastery": 0.05,
            "productive_struggle": 0.25,
            "confusion": 0.40,
            "disengagement": 0.15,
            "help_seeking": 0.15,
        }
    return {
        "mastery": 0.35,
        "productive_struggle": 0.30,
        "confusion": 0.15,
        "disengagement": 0.05,
        "help_seeking": 0.15,
    }


def _draw(probabilities: dict[str, float], rng: random.Random) -> str:
    draw = rng.random()
    cumulative = 0.0
    for state, probability in probabilities.items():
        cumulative += probability
        if draw <= cumulative:
            return state
    return next(reversed(probabilities))


def step(state: str, support: str = "none", seed=None) -> str:
    """Draw one learner state transition from the configured synthetic policy."""
    return _draw(_probabilities(state, support), random.Random(seed))


def simulate(start="productive_struggle", steps=20, support_policy=None, seed=42):
    """Simulate a reproducible learner trajectory with one persistent random stream."""
    if steps < 0:
        raise ValueError("steps must be non-negative")
    if start not in STATES:
        raise ValueError(f"unknown learner state: {start}")

    rng = random.Random(seed)
    state = start
    trajectory = [state]
    for _ in range(steps):
        support = support_policy(state) if support_policy else "none"
        state = _draw(_probabilities(state, support), rng)
        trajectory.append(state)
    return trajectory
