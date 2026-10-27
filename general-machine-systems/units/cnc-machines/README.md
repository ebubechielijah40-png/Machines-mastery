# Cnc Machines — mechanism, failure, and reconstruction

## Why this machine exists
CNC machines convert geometric toolpaths into controlled multi-axis motion and material removal.

## Energy and information path
Program → planner/interpolator → servo commands → motors/axes → tool-workpiece forces; encoders/limits close control/safety loops.

## Mechanism
Accuracy depends on kinematics, backlash, stiffness, thermal expansion, tool deflection and controller tuning.

When studying a real example, first draw the boundary and label energy input, useful output, losses, state, control, and interfaces. Then descend into the component that limits behavior instead of cataloguing parts.

## Failure modes
tool wear, collision, lost steps/servo faults, backlash, spindle failure

A failure is evidence about mechanism. Record symptom → competing hypotheses → measurement → result → revised model. Do not jump from symptom directly to replacement.

## Experiment
Simulate 2-axis interpolation of a circle and quantify discretization error.

Before measuring, predict the direction and approximate magnitude of the effect. Record units, uncertainty, and what the experiment cannot establish.

## Reconstruction challenge
Trace a dimensional defect to geometry, tool, mechanics, control, or thermal hypotheses.

After studying, hide the reference and redraw the functional block diagram from memory. Your reconstruction passes only if another person could use it to predict behavior under a changed load or failure.
