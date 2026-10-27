# Robot Arms — mechanism, failure, and reconstruction

## Why this machine exists
Robot arms position/orient tools by coordinating linked joints.

## Energy and information path
Motor torque → joints/links → end-effector motion; encoders provide joint state; controller closes the loop.

## Mechanism
Forward kinematics maps joint angles to pose; inverse kinematics seeks joint configurations for a pose and may have multiple/no solutions. Dynamics add mass/inertia/gravity.

When studying a real example, first draw the boundary and label energy input, useful output, losses, state, control, and interfaces. Then descend into the component that limits behavior instead of cataloguing parts.

## Failure modes
singularities, collision, backlash, overload, encoder error

A failure is evidence about mechanism. Record symptom → competing hypotheses → measurement → result → revised model. Do not jump from symptom directly to replacement.

## Experiment
Implement planar 2-link forward kinematics; map reachable workspace and solve selected inverse cases.

Before measuring, predict the direction and approximate magnitude of the effect. Record units, uncertainty, and what the experiment cannot establish.

## Reconstruction challenge
Reconstruct link lengths/joint axes from observed end-effector trajectories.

After studying, hide the reference and redraw the functional block diagram from memory. Your reconstruction passes only if another person could use it to predict behavior under a changed load or failure.
