## Step 3 — Open a pull request workflow

- **File**: `.github/workflows/3-open-a-pull-request.yml`
- **Purpose**: Advances the course from step 3 to step 4 when a pull request is opened or reopened from `my-first-branch`.

### Triggers
- `workflow_dispatch`
- `pull_request` with types: `opened`, `reopened`

### Permissions
- `contents: write`

### Jobs and flow
- `get_current_step`: Reads current step value.
- `on_open_a_pull_request` runs when:
  - Repository is not a template
  - `current_step == 3`
  - `github.head_ref == 'my-first-branch'`

Steps:
- Checkout repository with `ref: my-first-branch`
- Run `skills/action-update-step@v2`:
  - `from_step: 3`
  - `to_step: 4`
  - `branch_name: my-first-branch`

### Example: Open a pull request
- Via UI: Click "Compare & pull request" after pushing to `my-first-branch`.
- Via CLI:
```bash
gh pr create -B main -H my-first-branch \
  -t "Add my first file" \
  -b "Created PROFILE.md and proposed merging into main."
```

### Customization
- To allow other head branches, broaden the `if:` expression or remove the `github.head_ref` equality.
