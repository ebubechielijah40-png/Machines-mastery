# Push the GitHub-ready source

The current ZIP contains **only repository files, directly at its root**. Extract
all of it into your clone. There is no wrapper directory, Git bundle, release
receipt, checksum sidecar, cache or compiler distribution to delete before pushing.
Keep the separately supplied checksum and optional history bundle outside the clone.

## Git CLI, including Windows Git Bash or PowerShell

Start in the directory containing the downloaded ZIP. Clone the existing GitHub
repository so your new work keeps its history:

```sh
git clone https://github.com/ebubechielijah40-png/Machines-mastery.git Machines-mastery
cd Machines-mastery
git switch -c review/github-ready-2026-10-25
python -m zipfile -e ../Machines-mastery-development-2026-10-25.zip .
python tools/check_publication.py
git status --short
git diff --stat
git add --all
git commit -m "Refine Machines Mastery source and verification for publication"
git push -u origin review/github-ready-2026-10-25
```

On a system that uses `python3`, substitute that for `python`. If you already
have a clean clone, start at `git switch`; do not clone into that existing folder.
If your branch name already exists, choose a new review-branch name. Authenticate
with your own GitHub account when Git requests it. Open a pull request from that
branch to main after reviewing the changes. These instructions do not force-push
or overwrite main. Changes made on GitHub after this source checkpoint still need
normal conflict review; do not discard someone else's work.

The publication check is fast and checks the file tree. Full execution uses
[INSTALL_AND_RUN](INSTALL_AND_RUN.md); native laboratories have their own
toolchain/platform requirements. Optional tool absence is BLOCKED, not a pass.
The full educational mandate remains unfinished; publication readiness does
not change [the fixed33-domain quality gates](STRONG_PROGRESS_DASHBOARD.md).

## GitHub Desktop

Clone the existing repository, create a new review branch, and extract the ZIP
directly into that repository's local folder. Keep all extracted files, including
`.github`, `.gitignore` and `.gitattributes`. Review the Changes view, commit,
publish the review branch and open a pull request. No file cleanup is required.
Do not upload the ZIP itself as the repository's content.

## Optional: retain the complete development history

The separate `.bundle` is a recovery artifact, not a file to commit. If you want
the preserved development commits instead of a single source-overlay commit,
place the bundle outside your destination folder and use:

```sh
git clone --branch development/strong-priority-2026-10-25 Machines-mastery-development-2026-10-25-zip.bundle Machines-mastery-review
cd Machines-mastery-review
git remote rename origin delivered-checkpoint
git remote add origin https://github.com/ebubechielijah40-png/Machines-mastery.git
git fetch origin
git switch -c review/preserved-development-2026-10-25
git diff origin/main...HEAD --stat
git push -u origin review/preserved-development-2026-10-25
```

The bundle checkout already contains exactly the source represented by the ZIP;
extracting the ZIP into it is unnecessary. Keep the bundle outside the checkout.
No credentials are included in either artifact.
