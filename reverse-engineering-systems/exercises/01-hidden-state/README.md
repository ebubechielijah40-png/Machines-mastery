# Hidden-state investigation

Open [prompt.md](prompt.md) first. Do not browse `reveal/` or tests until you have saved hypotheses and attempted a replica. Source is hidden by study convention, not access control. Python 3.10+ standard library; no network or installation.

From repository root, run the public interface:

```sh
python3 reverse-engineering-systems/exercises/01-hidden-state/oracle.py
```

Enter one command per line: reset, up, down, or peek. EOF exits. Keep all observations, including errors. The same process preserves state between commands; a new process begins a fresh session. Shell redirection can save a session after you have learned that tool. The paper alternative is an assessor running your proposed queries without showing source.

After an independent attempt, run reference validation:

```sh
python3 -m unittest discover -s reverse-engineering-systems/exercises/01-hidden-state/tests -v
```

The exercise, oracle and reference are original assistant-created synthetic systems; no third-party target or claim of real-device behavior. Tests are executable reference validation, not learner progress.
