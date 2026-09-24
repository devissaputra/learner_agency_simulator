import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from learner_agency_simulator.core import simulate

print('Simulated learner trajectory:')
print(' -> '.join(simulate(steps=8)))
