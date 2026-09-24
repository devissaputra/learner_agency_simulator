# Ethics, safety, and misuse risks

## Intended use

Learner Agency Simulator is a synthetic research environment for exploring interactions between learner choices and adaptive support policies.

It is not a learner diagnosis tool, psychological assessment, recommendation engine, or validated digital twin of a person.

## Main risk: reifying synthetic labels

Terms such as `confusion`, `disengagement`, `persistence`, and `autonomy preference` can sound psychologically authoritative.

In this repository they are modeling abstractions.

Do not assign these simulator labels or parameter values to real learners unless a separate empirical study establishes a valid measurement model for the specific population and context.

## Agency and learner rights

A system claiming to support learner agency should not define agency as compliance with the system.

This simulator therefore makes learner requests and support refusal explicit.

A real adaptive system should also preserve meaningful learner choices, explain interventions where appropriate, and provide ways to override or opt out of recommendations.

## Over-support

More intervention is not automatically better.

A policy can reduce simulated confusion while also producing excessive unsolicited support. That may reduce autonomy, productive struggle, or trust in a real setting.

For this reason policy evaluation includes intervention burden and support refusal, not only mastery-like states.

## Under-support

An autonomy-preserving policy can also fail by withholding useful help.

Agency should not be used as a reason to abandon learners who need support.

Real systems need accessible ways to request help and should evaluate whether support options are understandable and genuinely available.

## Simulator exploitation

A policy may perform well because it exploits the simulator's hand-written transition rules rather than because the policy would help a real learner.

Policy conclusions should therefore be stress-tested across transition scenarios and validated independently before any deployment claim is made.

## Privacy

The current simulator requires no human data.

If empirical traces are later used for calibration, collect only what is necessary and apply appropriate governance to learning histories, support requests, demographic data, disability information, free text, or other sensitive records.

Do not increase surveillance merely to create a richer simulator.

## Fairness

Different learner groups may face different task structures, access barriers, prior opportunities, or support expectations.

Do not encode group stereotypes as agency profiles.

If group-level calibration is scientifically justified, document sample size, uncertainty, measurement validity, and potential harms.

## Uses excluded from this prototype

Do not use this repository alone for:

- psychological profiling
- labeling learners as disengaged or low-agency
- autonomous grading, admissions, discipline, or employment decisions
- withholding support from a learner
- covert experimentation
- claiming that one simulated policy is proven effective in real education
- optimizing for compliance with system recommendations

## Before a real-user study

Document the learning context, learner choice architecture, support options, consent or other lawful basis, measurement validity, privacy protections, human oversight, opt-out mechanisms, failure monitoring, accessibility, and the evidence required before changing real adaptive-support behavior.
