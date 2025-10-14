## API and component documentation

This repository is a GitHub Skills course template ("Introduction to GitHub"). Its public surface consists of GitHub Actions workflows that progress a learner through steps by editing `README.md`. There is no application runtime code; the "APIs" here are the workflows, their jobs, and the actions they invoke.

- **Scope**: Five workflows under `.github/workflows/` and step content under `.github/steps/`.
- **Audience**: Maintainers customizing the course and contributors operating the workflows.

### Contents
- **Workflows reference**
  - [Step 0 — Welcome](workflows/0-welcome.md)
  - [Step 1 — Create a branch](workflows/1-create-a-branch.md)
  - [Step 2 — Commit a file](workflows/2-commit-a-file.md)
  - [Step 3 — Open a pull request](workflows/3-open-a-pull-request.md)
  - [Step 4 — Merge your pull request](workflows/4-merge-your-pull-request.md)
- **Actions used**
  - [actions/checkout@v4 and skills/action-update-step@v2](../docs/actions.md)
- **Examples and usage**
  - [Run the course via UI or CLI](../docs/examples.md)
- **Troubleshooting**
  - [Common issues and fixes](../docs/troubleshooting.md)

### Quick start
- Ensure GitHub Actions are enabled for the repository.
- Follow the instructions in `README.md` to advance steps, or use the examples in [examples.md](../docs/examples.md).
- To customize branch naming or step flow, edit the conditions and inputs inside the workflow files documented above.
