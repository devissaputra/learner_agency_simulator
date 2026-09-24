# Research protocol

## Project

Learner Agency Simulator

## Questions

1. How do adaptive policies behave under diverse learner-state trajectories?
2. Which policies recover disengaged learners without over-supporting?
3. How sensitive are policy results to simulator assumptions?

## Baseline methods

- explicit learner states
- state transition probabilities
- support conditioned transitions
- reproducible simulation
- policy stress testing

## Evidence to collect

Start from the current transparent baseline and record every transformation needed to produce a reproducible sequence of synthetic learner states under an optional support policy. Keep a clear boundary between synthetic demonstration data and any future empirical dataset.

## Validation

Use empirical data only to calibrate or bound transition assumptions, then perform sensitivity analysis across plausible parameter ranges. Policy conclusions should be reported with uncertainty about the simulator itself.

## What counts as a useful result

The most useful next step is not more states. It is to fit or calibrate transition assumptions from empirical traces, then test whether candidate tutoring policies remain safe under plausible learner behavior variation.

## Threats to validity

State definitions can oversimplify learning, transition probabilities may not transfer across tasks, and a policy can look strong by exploiting unrealistic simulator assumptions.
