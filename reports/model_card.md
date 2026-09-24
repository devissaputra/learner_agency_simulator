# Simulation system card

## System

Learner Agency Simulator

## Purpose

A transparent stochastic environment for stress-testing interactions between synthetic learner choices and adaptive support policies.

## Current maturity

Working research prototype.

All states, profiles, transition probabilities, and policy effects are hand-specified simulation assumptions. The repository contains no empirical evidence that the simulator reproduces real learner behavior.

## State space

Current synthetic states:

- mastery
- productive struggle
- confusion
- disengagement

They represent task-level simulation states, not psychological diagnoses.

## Learner action space

The learner can:

- continue
- request hint
- request example
- change strategy
- choose easier task
- choose harder task
- pause
- decline support

## System action space

The system can offer:

- none
- guided hint
- worked example
- reflection prompt
- challenge

Learner requests can trigger hint/example support. A learner can reject proactive support.

## Agency profile

The current profile parameters are:

- help-seeking tendency
- support acceptance
- persistence
- challenge preference
- strategy switching
- autonomy preference

Each is bounded from 0 to 1 and changes the simulated learner-action distribution.

These are scenario controls only.

## Transition model

Every learner state has a distinct baseline next-state distribution.

Learner action modifies that distribution. Resolved system support modifies it again.

The transition matrix is validated before use.

## Outputs

A trajectory records:

- step
- current state
- learner action
- system offer
- resolved support
- next state

Aggregate policy evaluation reports:

- state occupancy
- mastery reach
- time to first mastery
- proactive interventions
- learner support requests
- accepted support
- declined support
- disengagement recovery

## Policy stress testing

Included policies are intentionally simple and inspectable.

The software can compare multiple policies over many deterministic seeds and can repeat those comparisons under modified confusion/disengagement persistence.

A policy result is a statement about the simulator configuration, not a real educational treatment effect.

## Main limitations

The current model:

- is a first-order Markov abstraction
- does not model knowledge components
- does not infer hidden states
- does not model peer/teacher co-agency
- does not learn parameters from data
- uses hand-written action and support effects
- does not represent long-term goals or curriculum structure
- does not estimate causal effects
- does not validate psychological constructs

## Evidence needed before real use

A serious empirical version would need construct definitions, observable mappings, calibration data, held-out validation, uncertainty around transition parameters, sensitivity studies, subgroup/fairness analysis where justified, and evidence that simulated policy conclusions predict anything useful in real settings.

## Human oversight

Researchers remain responsible for how states are defined, how profiles are interpreted, how policies are chosen, which metrics matter, which sensitivity scenarios are plausible, and whether any simulator result is appropriate to test with real learners.
