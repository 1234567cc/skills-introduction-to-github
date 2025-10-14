## Examples and usage

This repository is a tutorial course. Use these examples to simulate or automate the course progression.

### Start the course
- Push to `main` (empty commit is fine) to trigger Step 0 -> 1 advance:
```bash
git commit --allow-empty -m "Kick off course"
git push origin main
```

### Create the learner branch
```bash
git checkout -b my-first-branch
git push -u origin my-first-branch
```

### Make the first commit on the learner branch
```bash
echo "Welcome to my GitHub profile!" > PROFILE.md
git add PROFILE.md
git commit -m "Add PROFILE.md"
git push
```

### Open a pull request
```bash
gh pr create -B main -H my-first-branch \
  -t "Add my first file" \
  -b "Created PROFILE.md and proposed merging into main."
```

### Merge the pull request
```bash
gh pr merge --merge --delete-branch
```

### Rerun or debug workflows
- Manually dispatch any workflow from the Actions tab.
- Re-run failed jobs from the workflow run page.
