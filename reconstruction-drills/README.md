# Reconstruction from understanding

After a reviewed lesson, close the implementation and solutions; keep only the observable interface and task constraints. On a fresh page draw architecture, interfaces, data structures, control flow, state and a minimal implementation skeleton. Explain which choices are remembered, which derived and which uncertain. Do not peek and retrospectively call it recall.

Then compare against the reference and run fresh tests. Record: remembered correctly; derived correctly; missed; falsely assumed; conceptual reason for each error; smallest repair exercise. Use [record template](record.md). Repeat next session, after a week and after a month as a proposed cadence, adjusting to evidence. No time-based promotion.

First drill: recreate the Code decoder's state and boundaries with a different four-symbol table after CODE-01 study. Later: reconstruct the byte-parser preconditions; derive ADDI fields; draw the register's reset/enable priority. The reference stays present in the repository but closed during the attempt; no destructive removal is needed.

Ten levels: 1 observe; 2 explain; 3 reproduce; 4 reimplement; 5 break; 6 debug; 7 modify; 8 extend; 9 reconstruct without reference; 10 investigate an unfamiliar related system. Levels are practices, not automatically granted mastery states. Stages A/B/C/D remain reproduction/reimplementation/experimentation/extension; level 9 and 10 evidence strengthens later review rather than replacing earlier gates.
