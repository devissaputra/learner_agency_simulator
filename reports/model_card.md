# Analytic system card

## System

Learner Agency Simulator

## Purpose

Controllable stochastic learner state simulator for stress testing adaptive support policies.

## Current maturity

Working research prototype. The bundled example checks the software path with synthetic inputs. It does not establish validity for real learners, instructors, courses, or workplaces.

## Inputs

See `../data/README.md` for the current synthetic schema and the documentation expected before real data are connected.

## Outputs

The current code produces a reproducible sequence of synthetic learner states under an optional support policy. These outputs are research signals and should be interpreted with the educational context that produced them.

## Evidence needed before real use

Use empirical data only to calibrate or bound transition assumptions, then perform sensitivity analysis across plausible parameter ranges. Policy conclusions should be reported with uncertainty about the simulator itself.

## Main limitation

The state names and transition probabilities are modeling assumptions. They should never be interpreted as validated psychological states or individual diagnoses.

## Human oversight

A person must review any output before it can affect a learner, instructor, applicant, or employee.
