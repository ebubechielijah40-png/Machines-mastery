# Embedded/robotics experiments

- sensor noise: add Gaussian/uniform noise and compare raw vs filtered estimate;
- sample rate: change control-loop period and observe stability/lag;
- actuator saturation: clamp control and observe integral windup; design anti-windup;
- latency: insert delay between sensing and actuation;
- dropped samples: hold last value vs fail-safe behavior;
- calibration: add offset/scale error and estimate correction from reference points;
- battery/power constraint model: reduce available actuator authority over time;
- reconstruction: infer controller behavior from step-response data without seeing gains.

A simulator validates equations/code under its model; real robots add nonlinearities, backlash, compliance, friction, sensor physics, power electronics, and safety constraints.
