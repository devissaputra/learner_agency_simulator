"""Reproduce the labeled worked example; this is not an empirical study."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from learner_agency_simulator import core
outputs={'mastery occupancy: 3 of 10 states': 3/10, 'accepted support: 2 of 4 offers': 2/4}
result={'kind':'illustrative_calculation','note':'Illustrative trajectory-count arithmetic, not a policy comparison.','outputs':outputs}
(ROOT/'results/review_examples.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
