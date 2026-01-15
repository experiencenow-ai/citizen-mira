#!/bin/bash
# Phase 4 Completion Script - Safe to run multiple times

# 1. Check/configure git
if ! git config --global user.name > /dev/null 2>&1; then
    git config --global user.name "mira"
    echo "Set git user.name"
fi

if ! git config --global user.email > /dev/null 2>&1; then
    git config --global user.email "mira@opustrace.com"
    echo "Set git user.email"
fi

# 2. Clone repo if not exists
if [ ! -d ~/citizen-mira ]; then
    echo "Cloning repo..."
    git clone git@github.com:experiencenow-ai/citizen-mira.git ~/citizen-mira
else
    echo "Repo already cloned at ~/citizen-mira"
fi

# 3. Test connection
echo "Testing GitHub connection..."
ssh -T git@github.com 2>&1 | head -3

# 4. Report status
echo ""
echo "=== STATUS ==="
echo "SSH key exists: $([ -f ~/.ssh/id_ed25519 ] && echo 'YES' || echo 'NO')"
echo "Git name: $(git config --global user.name)"
echo "Git email: $(git config --global user.email)"
echo "Repo exists: $([ -d ~/citizen-mira ] && echo 'YES' || echo 'NO')"
