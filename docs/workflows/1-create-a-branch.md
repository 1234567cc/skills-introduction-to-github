## Step 1 — Create a branch workflow

- **File**: `.github/workflows/1-create-a-branch.yml`
- **Purpose**: Advances the course from step 1 to step 2 when the learner creates branch `my-first-branch`.

### Triggers
- `workflow_dispatch`
- `create` (branch or tag)

### Permissions
- `contents: write`

### Jobs and flow
- `get_current_step`: Same behavior as other steps; reads current step.
- `on_create_a_branch` runs when all are true:
  - Repository is not a template
  - `current_step == 1`
  - `github.ref_type == 'branch'`
  - `github.ref_name == 'my-first-branch'`

It then checks out the repo and runs `skills/action-update-step@v2` with:
- `from_step: 1`
- `to_step: 2`
- `branch_name: my-first-branch`

### Example: Creating the branch
- Via UI: Use the Code tab branch dropdown to create `my-first-branch`.
- Via CLI:
```bash
git checkout -b my-first-branch
git push -u origin my-first-branch
```

### Customization
- To support different branch names, update the `if:` conditions and the `branch_name` input consistently.
