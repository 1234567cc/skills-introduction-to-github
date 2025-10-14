## Troubleshooting

### Workflows not running
- Ensure Actions are enabled on the repository (Settings → Actions → General).
- Confirm triggers match your actions:
  - Step 0 and Step 4 require pushes to `main`.
  - Step 1 requires branch creation of `my-first-branch`.
  - Step 2 requires a push to `my-first-branch`.
  - Step 3 requires opening/reopening a PR from `my-first-branch`.

### "Current step" condition never matches
- Inspect `.github/steps/-step.txt`. Expected numeric step (`0`..`4`) or `X` at finish.
- The `get_current_step` job reads this file and sets `current_step`. Ensure the file exists and is tracked.

### Permission denied when updating README.md
- All workflows request `contents: write` permission. If you scoped the token, grant `contents: write`.
- Verify the workflow uses `${{ secrets.GITHUB_TOKEN }}` and that branch protection allows workflow commits.

### Branch name differs from `my-first-branch`
- Update both:
  - The `if:` expressions in workflows referencing `github.ref_name` or `github.head_ref`.
  - The `branch_name` input to `skills/action-update-step@v2`.

### Pull request events not checking out learner branch
- Under PR-triggered workflow, ensure checkout step includes `ref: my-first-branch` or uses `github.head_ref` dynamically.

### How to re-run Step N
- Manually dispatch the corresponding workflow from the Actions tab.
- Or modify triggers to allow your current state and push again.
