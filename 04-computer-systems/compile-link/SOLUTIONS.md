# Checkable solution notes

1. The declaration describes a callable interface; the definition supplies the
   actual body/storage. Neither alone proves memory safety of a call.
2. `sum_bytes` is undefined (`U`) in the caller object and code-defined (`T`) in
   the implementation under the observed GNU/ELF tools. Other formats can differ.
3. Sum256. The data region must permit three readable bytes and output must point
   to a live writable/aligned uint64_t; neither length nor pointer alone suffices.
4. Zero loop iterations require no data read. The output is always published on
   success, so it must exist even for the empty input.
5. Linking fails; recompiling the same declaration does not create a definition.
6. Effective-address arithmetic computes x+2x into the result register; adding y
   gives3x+y. The instruction does not dereference the calculated address.
7. Optimizers can keep values in registers or remove redundant storage while
   preserving valid program behavior. Debugger locations are not C semantics.
8. Set output=123, call sum_bytes(NULL,1,&output), require false and output123.
   An arbitrary invalid nonnull pointer is outside the defensive API contract.
9. Inspect the applicable target ABI's aggregate, vector/floating argument, return,
   variadic and stack/preserved-register rules. These were not verified here.
10. The retained reference log has both failure/success cases for comparison;
    exact temporary paths or instruction addresses need not match another run.
11–12. A new implementation must include independently specified vectors, a
   zero-length case, a caller violation boundary, source/version evidence and a
   limitation. Copying the reference and passing its cases is not unaided transfer.
