# Research protocol

## Project

Learner Agency Simulator

## Research questions

1. How do learner choices change the trajectory produced by an adaptive learning environment?
2. How do proactive system interventions compare with learner-requested support?
3. When does support improve simulated recovery from confusion or disengagement, and when does it create unnecessary intervention burden?
4. How sensitive are policy comparisons to assumptions about persistence, help seeking, support acceptance, challenge preference, strategy switching, and autonomy preference?
5. Do policy conclusions remain stable when confusion or disengagement is made more persistent?

## Current baseline

The simulator is a transparent stochastic environment with three separate layers:

1. **learner state**
2. **learner action**
3. **system action**

The current states are:

- mastery
- productive struggle
- confusion
- disengagement

The current learner actions are:

- continue
- request hint
- request example
- change strategy
- choose easier task
- choose harder task
- pause
- decline support

The current system actions are:

- none
- guided hint
- worked example
- reflection prompt
- challenge

A learner request can trigger support even when the system did not proactively offer it. A learner can also decline proactive support.

## Agency operationalization

This project does not define agency as a latent psychological score.

The current operationalization is narrower and observable within the simulator:

- selecting among learner actions
- requesting support
- refusing unsolicited support
- changing strategy
- changing task difficulty
- persisting or pausing

This is a modeling choice, not a validated theory of agency.

The simulator should therefore be described as an environment for testing how **learner choice mechanisms and adaptive system policies interact**, not as a model that measures real learner agency.

## Agency parameters

The synthetic profile currently contains six bounded parameters:

- help-seeking tendency
- support acceptance
- persistence
- challenge preference
- strategy switching
- autonomy preference

They alter action probabilities.

They are scenario parameters, not diagnoses or psychometric scales.

## State dynamics

The four learner states have distinct baseline transition distributions.

Learner actions modify the transition distribution. Resolved system support modifies it again before the next state is sampled.

Every transition matrix is validated so that probabilities are finite, non-negative, defined for all states, and sum to one.

## Policies

The repository includes four transparent policy examples:

- no proactive support
- hint when confused
- hint when disengaged
- autonomy-preserving policy that uses a reflection prompt only when disengaged

These are intentionally simple control policies.

A policy receives the current state and simulation history and returns a system action.

## Stress testing

`evaluate_policy()` runs one policy across many deterministic seeds.

`compare_policies()` evaluates multiple policies under the same simulation settings.

Current policy metrics include:

- mastery occupancy
- productive-struggle occupancy
- confusion occupancy
- disengagement occupancy
- fraction of runs that reach mastery
- mean time to first mastery
- mean number of proactive system interventions
- mean number of learner support requests
- mean accepted support
- mean declined support
- disengagement recovery rate

These metrics describe simulator behavior only.

## Sensitivity analysis

`perturb_transition_matrix()` changes confusion or disengagement persistence while preserving a valid transition matrix.

`sensitivity_study()` repeats policy comparisons under several simulator scenarios:

- baseline
- stickier disengagement
- stickier confusion
- more recoverable difficulty

A useful simulator result is not "Policy X wins."

A useful result is evidence about **which policy conclusions remain stable, which reverse, and which depend strongly on hand-written behavioral assumptions**.

## Reproducibility

A single random stream is used inside each trajectory.

Policy evaluation uses deterministic seed sequences so the same configuration produces the same aggregate results.

Seeds should be reported with any simulation study.

## Empirical calibration

Future empirical work should separate calibration from validation.

A credible study would:

1. define observable proxies for state and learner action
2. estimate transition ranges from a calibration dataset
3. quantify uncertainty in those estimates
4. reserve held-out data for simulator validation
5. test whether simulated transition frequencies resemble held-out trajectories
6. repeat policy stress tests over plausible parameter ranges rather than a single fitted model

## Evaluation design

Compare candidate policies across multiple profiles, transition scenarios, and seeds.

Report:

- means
- dispersion or uncertainty across runs
- intervention burden
- support refusal/request behavior
- policy rank reversals across assumptions
- failure cases

Do not report a single policy score as if it were an empirical learner outcome.

## Threats to validity

Major threats include:

- state definitions that oversimplify learning
- agency parameters without construct validity
- transition probabilities chosen for convenience
- policy effects encoded too directly into the simulator
- unrealistic independence assumptions
- no representation of content difficulty or knowledge components
- no social/contextual co-agency
- simulator exploitation, where a policy performs well by taking advantage of artifacts of the model
- conclusions that fail when transition assumptions change

The simulator is useful precisely when these assumptions remain inspectable and can be perturbed.
