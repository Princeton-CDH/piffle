#!/bin/sh
#
# Set up custom git-flow workflow by updating git-flow configuration

# Set custom git-flow hooks path
git config gitflow.path.hooks gitflow-hooks

# Always fetch before release operations
git config gitflow.release.fetch true

# Fetch from remote before creating topic branch
git config gitflow.feature.start.fetch true
git config gitflow.hotfix.start.fetch true
git config gitflow.bugfix.start.fetch true

# Use custom message for develop auto-updates
git config gitflow.hotfix.finish.updatemessage "chore: sync %b from %p"
git config gitflow.release.finish.updatemessage "chore: sync %b from %p"
