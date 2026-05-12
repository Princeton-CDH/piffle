#!/bin/sh
#
# Set up custom git-flow workflow by updating git-flow configuration

# Set custom gitflow hooks path
git config gitflow.path.hooks gitflow-hooks

# Fetch from remote before creating topic branch
git config gitflow.feature.start.fetch true
git config gitflow.release.start.fetch true
git config gitflow.hotfix.start.fetch true
git config gitflow.bugfix.start.fetch true

# Use squash merge for hotfixes and releases
git config gitflow.branch.hotfix.upstreamStrategy squash
git config gitflow.branch.release.upstreamStrategy squash

# Always fetch before release operations
git config gitflow.release.fetch true

# Use custom message for develop auto-updates
git config gitflow.hotfix.finish.updatemessage "chore: sync %b from %p"
git config gitflow.release.finish.updatemessage "chore: sync %b from %p"
