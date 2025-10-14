## Step 0 — Welcome workflow

- **File**: `.github/workflows/0-welcome.yml`
- **Purpose**: Initializes the course and advances the repository from step 0 to step 1 by updating `README.md` on first push to `main` (or manual dispatch).

### Triggers
- `workflow_dispatch`
- `push` on branch `main`

### Permissions
- `contents: write` (required to update `README.md`)

### Jobs and flow
- `get_current_step`
  - Checks out the repo and reads `./.github/steps/-step.txt` to determine the current step number.
  - Exposes `current_step` as a job output.
- `on_welcome`
  - Runs only if the repository is not a template and `current_step == 0`.
  - Checks out the repo and invokes `skills/action-update-step@v2` with inputs:
    - `token: ${{ secrets.GITHUB_TOKEN }}`
    - `from_step: 0`
    - `to_step: 1`
    - `branch_name: my-first-branch`

### Example: Manual run
Use the Actions tab to run the workflow manually via the `Run workflow` button. A subsequent push to `main` will also trigger it.

### Customization
- Change the learner branch by editing `branch_name` input.
- To alter when the first advance happens, adjust the `on:` triggers or the `if:` expression guarding `on_welcome`.

### Related components
- Reads step state from `.github/steps/-step.txt`.
- Updates content in `README.md`.
