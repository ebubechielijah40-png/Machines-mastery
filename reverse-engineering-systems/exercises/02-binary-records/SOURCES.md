# Sources and evidence boundaries

The oracle C source, wrapper, record layout, worked probes and Python
reconstruction are original repository teaching code. No external protocol,
firmware or industrial reverse-engineering result is claimed. The exact source
and compiled binary hashes and compiler command are retained in
[evidence/observed.json](evidence/observed.json); these12 probes were actually run.

Primary reference inspected2026-10-23: Python Software Foundation,
[Python3.12 binascii documentation](https://docs.python.org/3.12/library/binascii.html),
`crc_hqx(data,value)` entry, live page identifying3.12.15. It specifies the
x^16+x^12+x^5+1 polynomial/0x1021 and caller-supplied initial value used for the
independent CRC test oracle. Our encoding convention, initialffff, byte order
and rejection policy are defined by this original target, not attributed to a
standard CRC name. The documentation is referenced, not copied into this unit.

C code explicitly serializes bytes and converts the signed sample to uint16_t;
it never transmits a host struct. The native differential and sanitizer tests
support finite behavioral observations. Source inspection after the attempt
confirms what this supplied target does; black-box finite observations alone
cannot uniquely identify an arbitrary unknown implementation.
