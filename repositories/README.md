# Repository Study

[REPOSITORY_REGISTRY.md](../REPOSITORY_REGISTRY.md) lists identified upstream repositories. No checkout has been made and no implementation behavior is verified.

When study begins, use an ignored `checkouts/<slug>/` directory, record upstream URL and exact commit, and inspect README, LICENSE/NOTICE and build instructions before executing anything. Do not recurse into or modify unrelated local repositories. Fetch only the selected project, not the whole registry.

Start from [templates/repository-study.md](../templates/repository-study.md). Establish purpose, architecture, entry points, components, control flow, data flow, structures, interfaces, dependencies, state, storage, networking, security boundaries and tests. Trace one meaningful operation end-to-end with commit, path and symbol references.

Record original creators separately from repository account ownership. A repository listing or README is insufficient evidence for claims about implementation behavior. Pin dependencies and note sandbox/environment requirements before running local builds.
