## Step 4 — Merge your pull request workflow

- **File**: `.github/workflows/4-merge-your-pull-request.yml`
- **Purpose**: Advances the course from step 4 to step X after a push to `main` (typically caused by merging the PR).

### Triggers
- `workflow_dispatch`
- `push` on branch `main`

### Permissions
- `contents: write`

### Jobs and flow
- `get_current_step`: Reads current step value.
- `on_merge_your_pull_request` runs when:
  - Repository is not a template
  - `current_step == 4`

Steps:
- Checkout repository
- Run `skills/action-update-step@v2`:
  - `from_step: 4`
  - `to_step: X`
  - `branch_name: my-first-branch`

### Example: Merge the PR
- Via UI: Click "Merge pull request" on your PR into `main`.
- Via CLI:
```bash
gh pr merge --merge --delete-branch --admin
```

### Customization
- To progress to a different final state, change `to_step` to a number or another marker.
