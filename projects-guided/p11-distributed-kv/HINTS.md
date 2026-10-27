# Hints after a design attempt

A received assignment is another overwrite; changing its order changes a blind
map. A maximum of the same stamped record set does not depend on that ordering.
Keep the winner as a record rather than discarding its stamp. Missing and a
higher-stamp deletion must remain distinguishable. A repeated delivery may
leave the map unchanged while advancing the receiver clock. Build and validate
a candidate transition before replacing current state. Carry the sender's event
stamp separately when local events were not writes. A valid signature would
not prove a legitimate node used a sensible counter or preserved a bank invariant.
