# Six connected implementation milestones

1. **Declare a plant boundary.** Positive current generates positive shaft torque;
   load torque opposes positive motion. Write v=Ri+L di/dt+kω and
   J dω/dt=ki−bω−load, dθ/dt=ω. Annotate every parameter/unit. Derive
   dE/dt=vi−Ri²−bω²−load·ω. Hand case i1A,ω3rad/s,v6V,load.01N·m gives
   di/dt185A/s, dω/dt1.5rad/s² and dE/dt3.79W for reference parameters.
2. **Integrate before controlling.** Implement the derivative, then RK4 under a
   constant command over each sample. Validate the k=0 decoupled case against
   exact RL/mechanical exponentials. Step refinement cannot replace checking
   equations. Reject nonfinite inputs and nonpositive time steps.
3. **Sense a history.** Add a seeded noise source, bias, quantization and integer
   delay. With delay2, noiseless samples[1,2,3,4] return[1,1,1,2] using first-sample
   prehistory. State that convention and Python's quantization tie behavior.
4. **Add controller memory.** Implement P, then integral z_next=z+error·dt,
   then derivative on measurement and its filter. Demonstrate a target step
   does not create derivative kick. Command clamps at±6V; integral clamping is
   a separate decision. Permit integration that helps leave saturation.
5. **Challenge feasibility.** Derive maximum no-load steady speed12rad/s at6V.
   Demand20rad/s for4s, then2rad/s. Compare integral state and post-switch
   true-speed error for identical gains with/without conditional integration.
   Add bias, delay and noise one at a time. Record unexpected outcomes too.
6. **Reconstruct and transfer.** Rebuild the equations and update order without
   notes. Add a load step and predict current/speed signs. Reflect a load inertia
   through G=4 using J_load/G². Explain why gear torque gain does not create power.

Milestone outputs are bounded mechanisms and causal evidence. A green tuned
trajectory without energy/analytic tests is insufficient. Close the reference
implementation until a milestone's derivation and prediction are written.
