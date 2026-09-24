# Data documentation

## Included data

`sample.csv` contains five **synthetic simulator profiles**. They are scenario configurations, not learner records and not validated psychological profiles.

No human-subject data are included.

## Profile schema

Each parameter is constrained to the interval 0–1:

- `help_seeking_tendency`: increases the simulated probability of requesting a hint or example when difficulty is present
- `support_acceptance`: affects how a learner responds when the system proactively offers support
- `persistence`: increases the simulated tendency to continue through difficulty
- `challenge_preference`: increases the simulated tendency to choose harder tasks
- `strategy_switching`: increases the simulated tendency to change approach when difficulty persists
- `autonomy_preference`: increases the simulated tendency to decline unsolicited support

These parameters are mechanisms for **scenario stress testing**. They must not be interpreted as diagnostic traits, stable personality measurements, or estimates about a real person.

## Learner states

The current simulator uses four synthetic task states:

- `mastery`
- `productive_struggle`
- `confusion`
- `disengagement`

The labels are modeling abstractions. The simulator does not infer them from real learner behavior.

## Learner actions

The simulated learner can:

- continue
- request a hint
- request an example
- change strategy
- choose an easier task
- choose a harder task
- pause
- decline offered support

This action layer is the repository's current operationalization of agency: the learner is not merely moved between states by the system.

## System actions

The simulated system can offer:

- no intervention
- guided hint
- worked example
- reflection prompt
- challenge

Learner requests can also trigger hint/example support when the system did not proactively offer it.

A learner may decline proactive support.

## Transition assumptions

`BASE_TRANSITIONS` contains the baseline state-to-state probabilities.

The transition matrix is fully validated:

- every state must be present
- every row must include every possible next state
- each probability must be finite and between 0 and 1
- every row must sum to 1

Learner actions and resolved system support then modify those baseline probabilities before the next state is sampled.

## Sensitivity scenarios

The included stress-test utilities can perturb confusion and disengagement persistence.

This is important because a policy that looks strong only under one hand-written simulator configuration is not robust evidence.

## If empirical data are used later

Separate **calibration** from **validation**.

Document:

- population and context
- what observable behavior corresponds to each modeled state
- how learner actions are observed
- how transitions are estimated
- uncertainty in transition estimates
- whether different groups require different parameter ranges
- held-out validation data
- missingness and censoring
- task/course differences
- intervention logging
- consent or other lawful basis
- permitted uses

Do not map behavioral traces directly to psychological labels without construct validation.

## Do not commit

Do not commit identifiable learner histories, raw LMS exports, disability or health information, private messages, raw student submissions, audio/video, or licensed datasets that prohibit redistribution.
