---
name: piffle release checklist
about: Checklist for releasing new versions of piffle
title: piffle release checklist
labels: chore
assignees: ''
---

## release prep

- [ ] Pull updated copies of the develop and main branches
- [ ] Use git-flow to create a new release branch with the appropriate version (e.g., `git flow release start 0.5`)
- [ ] Update release version to appropriate number (set to final version without any `-pre` or `-dev` tags).
- [ ] Create a PR for the release (from release branch to `main`)
- [ ] Review the changelog to make sure that all features, changes, bugfixes, etc. included in the release are documented. You may want to review the git revision history to be sure you've captured everything.
- [ ] Confirm that all checks for the PR pass (e.g., unit tests, code coverage checks)
- [ ] Review code documentation to make sure it is up to date
- [ ] Request a review for the PR
- [ ] Once approved, use git-flow to finish the release (`git flow release finish`).
  *Make sure to use the `--squash-message` flag to customize the commit message for the squash merge and
  the `--message` flag to specify the tag message.*

## after release

- With `post-release-update` feature branch (automatically created for you by git flow)
  - [ ] Increase the develop branch version so it is set to the next expected release (i.e., if you just released 0.5 then develop will probably be 0.6-dev unless you are working on a major update, in which case it will be 1.0-dev)
  - [ ] Update the changelog to include a section for the next expected release version
  - [ ] Create a PR and request a review once all checks are passing
- [ ] Push main branch updates to GitHub (`git push main`).
  *This will fail if the release's PR has not been approved or has failing checks.*
- [ ] Push tag to GitHub (e.g., `git push origin tag 0.5`)
- [ ] Create release on GitHub
- [ ] Merge `post-release-update` to develop.
  *This will fail if the feature's PR has not been approved or has failing checks.*
