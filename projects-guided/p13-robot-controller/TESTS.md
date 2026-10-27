# Validate the mechanism independently

From the repository root:

```sh
python3 -m unittest discover -s 17-embedded-robotics/control-path -p 'test_*.py' -v
python3 17-embedded-robotics/control-path/experiment.py
```

The actual [transcript](../../17-embedded-robotics/control-path/evidence/tests.txt)
contains ten passing tests. Hand derivative values and the energy-power identity
validate signs/units. The k=0 special case has independent analytic exponential
solutions, not just an alternate numerical method. Gear tests compare kinetic
energies under the speed ratio. Sensor tests use explicit delay vectors and
seed repeatability. Controller tests check saturation memory, derivative-kick
avoidance, recovery from a deliberately infeasible target and invalid-input
state preservation.

Add one unseen load-torque hand case and one equilibrium test in your learner
build. Halving dt should improve an open-loop smooth integration against an
analytic oracle; in a sampled closed loop it also changes the controller, so do
not call that difference pure integration error. A stable trace is evidence for
one model/setting, not a proof of stability for every motor/gain/delay.
