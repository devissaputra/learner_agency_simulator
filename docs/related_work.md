# Related work and methodological context

Learner Agency Simulator is an original implementation. It does not claim to reproduce a validated model of learner agency.

The references below motivate the distinction between **learners acting** and learners merely being acted upon.

## Student agency

The OECD Learning Compass 2030 treats student agency as involving learners' capacity and will to influence their lives through goal setting, reflection, responsible action, and meaningful choices.

- OECD Learning Compass 2030: https://www.oecd.org/en/data/tools/oecd-learning-compass-2030.html
- OECD Future of Education and Skills 2030/2040: https://www.oecd.org/en/about/projects/future-of-education-and-skills-2030.html

This repository does not attempt to encode the full OECD construct.

Instead, it operationalizes a narrow subset that can be represented transparently in simulation: requesting help, refusing support, changing strategy, persisting, pausing, and changing task challenge.

## Self-regulated learning

Self-regulated learning research provides a broader theoretical context for strategy choice, monitoring, motivation, and learner control.

- Zimmerman BJ. *Becoming a Self-Regulated Learner: An Overview.* Theory Into Practice. 2002. DOI: https://doi.org/10.1207/S15430421TIP4102_2
- Panadero E. *A Review of Self-regulated Learning: Six Models and Four Directions for Research.* Frontiers in Psychology. 2017. DOI: https://doi.org/10.3389/fpsyg.2017.00422

Panadero's review emphasizes that SRL spans cognitive, metacognitive, behavioral, motivational, and affective processes. The simulator intentionally represents only a small observable-action subset.

## Why separate learner action from system action

Adaptive-learning simulations can become system-centric if every transition is determined by the tutor policy.

This repository instead keeps three variables separate:

1. current learner state
2. learner action
3. system action

The system can offer support, the learner can request support, and the learner can refuse support.

That separation makes autonomy-related trade-offs visible in policy stress tests.

## Simulation as a policy test bed

A simulator can help discover brittle policies before a live study, but simulated policy performance is only as credible as the simulator assumptions.

The repository therefore focuses on:

- explicit transition matrices
- explicit learner-action probabilities
- multi-seed evaluation
- intervention-burden metrics
- sensitivity to altered state persistence
- transparent failure modes

## Scope boundary

Implemented:

- four synthetic task states
- eight learner actions
- five system actions
- synthetic agency parameters
- support acceptance/refusal
- state/action-conditioned transition changes
- multi-run policy evaluation
- policy comparison
- transition sensitivity scenarios

Not implemented:

- validated psychological measurement
- knowledge tracing
- content-specific skill states
- social/co-agency with peers or teachers
- learned transition models
- reinforcement-learning policy optimization
- partially observable state inference
- real learner calibration
- causal estimates of policy effects
