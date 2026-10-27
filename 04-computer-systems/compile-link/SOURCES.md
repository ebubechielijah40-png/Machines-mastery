# Source inspection — 2026-10-22

Original examples/code/prose; no source figures or passages copied. Public access
is not a redistribution license. No commercial book original was present.

| ID | Primary/official source and inspected locator | Scope |
| --- | --- | --- |
| S-COMPILER | GCC manual, [Overall Options](https://gcc.gnu.org/onlinedocs/gcc/Overall-Options.html), opening pipeline description and `-E`, `-S`, `-c`, `-o` entries | Stage/output controls; actual executable behavior is tested separately |
| S-NM | GNU Binutils manual, [nm](https://sourceware.org/binutils/docs/binutils/nm.html), opening symbol fields and B/D/T/U descriptions | How this tool labels symbols; not a complete C or ELF specification |
| S-OBJDUMP | GNU Binutils manual, [objdump](https://sourceware.org/binutils/docs/binutils/objdump.html), opening purpose and `-d`, `-r` option entries | Inspection controls; no source-code reuse |

Actual compiler is pinned by its version output in `evidence/observed.json`.
The online manuals are mutable and no byte snapshot or full license audit was
retained. The formal ELF gABI URL at Linux Foundation returned access denied;
the attempted x86-64 psABI PDF endpoint failed. Those specifications are
**UNVERIFIED — verification required**. Architecture-specific relocation/register
statements here are explicitly observations of our owned compiler output, not
claims of formal ABI compliance or a freshly verified complete specification.

## Additional inspected C and tool scopes — 2026-10-23

- WG14 [N1570, 2011-04-12 committee draft](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), §6.2.4 paragraphs1–7 (object lifetime), §6.2.8 paragraphs1–3 (alignment), §6.5 paragraphs5–7 (expression representability and effective type), §6.5.6 paragraphs8–9 (array pointer arithmetic), §7.22.3. These were inspected as a C11-era draft, not the latest standard or all defect reports. They support the lesson's pointer/lifetime and arithmetic caveats; no substantial passages are reproduced.
- GNU binutils official [readelf manual](https://sourceware.org/binutils/docs/binutils/readelf.html), “readelf” introduction and `-r`/`--relocs`, `-W`/`--wide` entries. These support the inspection flags; observed relocation names and values remain local evidence rather than a complete ELF specification reconstruction. Live manual inspected on the stated date; no upstream byte hash or matching local manual version is claimed.
