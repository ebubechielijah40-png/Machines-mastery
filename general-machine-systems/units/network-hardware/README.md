# Network Hardware — mechanism, failure, and reconstruction

## Why this machine exists
Network hardware forwards, filters or transforms traffic at line rates according to tables/protocol state.

## Energy and information path
Electrical/optical signal → PHY → frames/packets → lookup/classification → buffering/scheduling → output link.

## Mechanism
Switches use MAC tables; routers use forwarding tables; queues absorb bursts but create latency/drop under overload.

When studying a real example, first draw the boundary and label energy input, useful output, losses, state, control, and interfaces. Then descend into the component that limits behavior instead of cataloguing parts.

## Failure modes
link failure, buffer overflow, table errors, control-plane failure, power/thermal faults

A failure is evidence about mechanism. Record symptom → competing hypotheses → measurement → result → revised model. Do not jump from symptom directly to replacement.

## Experiment
Simulate a finite queue under burst traffic and observe delay/drop as arrival rate approaches service rate.

Before measuring, predict the direction and approximate magnitude of the effect. Record units, uncertainty, and what the experiment cannot establish.

## Reconstruction challenge
Infer a black-box network device role from ports, ARP/routing behavior and packet traces in an authorized lab.

After studying, hide the reference and redraw the functional block diagram from memory. Your reconstruction passes only if another person could use it to predict behavior under a changed load or failure.
