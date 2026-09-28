# Repository Guidelines

## Project Structure & Module Organization

This repository is a learning and research workspace. Its numbered subject directories run from `01-computation/` through `17-research/`, covering programming, systems, data science, security, machine learning, and related fields. These directories are currently empty; place topic-specific notes and exercises in the matching subject directory.

Use `books/` for reading notes, `experiments/` for focused investigations, and `projects/` for larger implementations. The root Markdown files are currently empty placeholders with these intended roles:

- `MASTER_CURRICULUM.md`: learning sequence and objectives.
- `KNOWLEDGE_GRAPH.md`: relationships and prerequisites between topics.
- `PROGRESS.md`: completed work and next steps.
- `SOURCES.md`: references and source links.

No source-code, test, or asset layout is established yet. Keep future implementation files, tests, and assets together within their project or experiment.

## Build, Test, and Development Commands

There is no repository-wide build system, dependency manifest, or development server. Useful repository checks include:

- `git status --short`: review changed and untracked files.
- `git diff --check`: check tracked changes for whitespace errors.
- `git diff --cached --check`: check staged contributions before committing.

When adding runnable code, include a local `README.md` with prerequisites and exact setup, run, and test commands.

## Coding Style & Naming Conventions

Use descriptive Markdown headings, fenced code blocks with language labels, and relative links to repository files. Indent nested lists consistently with two spaces. Preserve the numbered, lowercase, hyphenated subject-directory pattern; use descriptive filenames such as `memory-hierarchy.md`.

No formatter, linter, or language-specific style is configured. Document those choices locally when introducing code.

## Testing Guidelines

No testing framework or coverage threshold exists. Review Markdown rendering, verify links and citations, and check examples for accuracy. For executable projects, document the chosen test framework, test filenames, and test command alongside the implementation.

## Commit & Pull Request Guidelines

There are no commits yet, so no historical message convention exists. Use concise, imperative subjects, such as `Add networking study notes`. Keep each commit focused on one topic or change.

Pull requests should describe the purpose, affected topics or projects, and validation performed. Link relevant issues when available; include screenshots when changing visual output.
