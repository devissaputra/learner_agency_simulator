# Calculation guide

## Question and evidence

What do support policies imply under stated transition assumptions?

Synthetic state-transition matrices, learner preferences and support policies.

**Status:** SYNTHETIC / RULE-BASED PROTOTYPE | no educational validity claim.

## Design

Simulate learner choices and accepted/declined support; compare policies over seeds and perturbed transition assumptions.

## Calculation and interpretation

`State occupancy = observations in state / all recorded states.`

The initial state is included in occupancy; transition counts exclude it. Policy differences are consequences of the specified simulator, not estimated effects in real learners. Sensitivity to the transition assumptions is central.

## Evidence table

Worked example — illustrative, not a measured research result. Full precision below is for traceability, not a claim of measurement precision.

| Quantity | Value | Unit / meaning | JSON path |
|---|---:|---|---|
| mastery occupancy: 3 of 10 states | 0.3 | unitless | `outputs.mastery occupancy: 3 of 10 states` |
| accepted support: 2 of 4 offers | 0.5 | unitless | `outputs.accepted support: 2 of 4 offers` |

Source: [results/review_examples.json](results/review_examples.json). Values resolve directly from this file when figures are regenerated.

This simulator compares support policies while allowing synthetic learners to request, accept, or decline help. It tracks state occupancy, intervention burden, recovery, and time to first mastery across seeded trajectories and sensitivity scenarios. The outcomes reveal what the chosen transition assumptions imply; they do not establish that a policy improves agency or learning outside the simulation.

## Verification performed in this review

33 existing unittest checks passed. The bundled demonstration executed successfully in this review.

The figure-generation check verifies agreement between the selected source values and SVGs. It does not validate the raw dataset, fitted model, identification assumptions, or external generalization.

```bash
python scripts/build_review_figures.py
python scripts/build_review_figures.py --check
```

For the explicitly illustrative example:

```bash
python scripts/review_examples.py
```

## Implementation map

Follow these functions to inspect each transformation. Validation helpers and private functions remain visible in the linked modules.

| Function | Purpose / documented behavior |
|---|---|
| [`validate_transition_matrix`](src/learner_agency_simulator/core.py#L83) | Inspect the explicit implementation and its callers. |
| [`validate_agency_profile`](src/learner_agency_simulator/core.py#L109) | Inspect the explicit implementation and its callers. |
| [`learner_action_probabilities`](src/learner_agency_simulator/core.py#L166) | Inspect the explicit implementation and its callers. |
| [`choose_learner_action`](src/learner_agency_simulator/core.py#L249) | Inspect the explicit implementation and its callers. |
| [`resolve_support`](src/learner_agency_simulator/core.py#L268) | Inspect the explicit implementation and its callers. |
| [`transition_probabilities`](src/learner_agency_simulator/core.py#L286) | Inspect the explicit implementation and its callers. |
| [`step`](src/learner_agency_simulator/core.py#L388) | Inspect the explicit implementation and its callers. |
| [`no_support_policy`](src/learner_agency_simulator/core.py#L405) | Inspect the explicit implementation and its callers. |
| [`confusion_hint_policy`](src/learner_agency_simulator/core.py#L409) | Inspect the explicit implementation and its callers. |
| [`disengagement_hint_policy`](src/learner_agency_simulator/core.py#L413) | Inspect the explicit implementation and its callers. |
| [`autonomy_preserving_policy`](src/learner_agency_simulator/core.py#L417) | Inspect the explicit implementation and its callers. |
| [`simulate`](src/learner_agency_simulator/core.py#L423) | Simulate learner choices, system offers, resolved support, and state transitions. |
| [`trajectory_metrics`](src/learner_agency_simulator/core.py#L491) | Inspect the explicit implementation and its callers. |
| [`evaluate_policy`](src/learner_agency_simulator/core.py#L559) | Inspect the explicit implementation and its callers. |
| [`compare_policies`](src/learner_agency_simulator/core.py#L620) | Inspect the explicit implementation and its callers. |
| [`perturb_transition_matrix`](src/learner_agency_simulator/core.py#L634) | Inspect the explicit implementation and its callers. |
| [`sensitivity_study`](src/learner_agency_simulator/core.py#L690) | Inspect the explicit implementation and its callers. |
| [`mean`](src/learner_agency_simulator/core.py#L585) | Inspect the explicit implementation and its callers. |
| [`shift_persistence`](src/learner_agency_simulator/core.py#L656) | Inspect the explicit implementation and its callers. |

## What remains before a stronger research claim

The initial state is included in occupancy; transition counts exclude it. Policy differences are consequences of the specified simulator, not estimated effects in real learners. Sensitivity to the transition assumptions is central. A successful software test is not validation of a scientific construct. New experiments should state their split unit, comparator, outcome, uncertainty procedure and failure criteria before examining final test results.
