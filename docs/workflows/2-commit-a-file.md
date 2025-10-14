## Step 2 — Commit a file workflow

- **File**: `.github/workflows/2-commit-a-file.yml`
- **Purpose**: Advances the course from step 2 to step 3 when a commit is pushed to `my-first-branch`.

### Triggers
- `workflow_dispatch`
- `push` on branch `my-first-branch`

### Permissions
- `contents: write`

### Jobs and flow
- `get_current_step`: Reads current step value.
- `on_commit_a_file` runs when:
  - Repository is not a template
  - `current_step == 2`

Steps:
- Checkout repository (with full history)
- Run `skills/action-update-step@v2`:
  - `from_step: 2`
  - `to_step: 3`
  - `branch_name: my-first-branch`

### Example: First commit on the learner branch
```bash
echo "Welcome to my GitHub profile!" > PROFILE.md
git add PROFILE.md
git commit -m "Add PROFILE.md"
git push
```

### Customization
- To react to different branches, change the `on.push.branches` list.
