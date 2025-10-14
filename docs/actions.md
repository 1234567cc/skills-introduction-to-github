## Actions used in this course

### actions/checkout@v4
- Checks out the repository content so subsequent steps can read and modify files.
- Common inputs used here:
  - `fetch-depth: 0` to fetch all branches and history.
  - `ref: my-first-branch` when operating on a non-default branch under PR events.

### skills/action-update-step@v2
- A custom action that updates the learner's step in this repository by editing `README.md` and step metadata.
- Inputs used in this repo:
  - `token`: `${{ secrets.GITHUB_TOKEN }}` — required to commit changes.
  - `from_step`: numeric or letter indicating the current step.
  - `to_step`: numeric or letter for the next step.
  - `branch_name`: `my-first-branch` — the learner's branch name used by the content.

### Permissions model
All workflows request `contents: write` to allow committing `README.md` updates. If you fork this template and want read-only operation, remove or modify steps that write to the repo.
