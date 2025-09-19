#!/usr/bin/env bash
set -euo pipefail

# Default remote (change if you want)
DEFAULT_REMOTE="https://github.com/debasish-panda-22/hianime_api_full.git"

usage() {
  cat <<EOF
Usage: $0 [--remote <url>] [--yes] [--force-push]
  --remote <url>   : Git remote URL to push to (default: $DEFAULT_REMOTE)
  --yes            : skip interactive confirmation
  --force-push     : if push is rejected, force push to remote (destructive)
EOF
  exit 1
}

# parse args
REMOTE="$DEFAULT_REMOTE"
AUTO_YES=0
FORCE_PUSH=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --remote) REMOTE="$2"; shift 2;;
    --yes) AUTO_YES=1; shift;;
    --force-push) FORCE_PUSH=1; shift;;
    -h|--help) usage;;
    *) echo "Unknown arg: $1"; usage;;
  esac
done

# Safety: must run in a directory with files expected
PROJECT_ROOT="$(pwd)"
PROJECT_NAME="$(basename "$PROJECT_ROOT")"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
BACKUP_DIR="../${PROJECT_NAME}_git_backup_${TIMESTAMP}"

echo "PROJECT_ROOT: $PROJECT_ROOT"
echo "Backup directory for .git metadata will be: $BACKUP_DIR"
echo "Remote to add: $REMOTE"
echo

if [[ $AUTO_YES -ne 1 ]]; then
  read -rp "This will remove all git metadata from this working copy and create a NEW git repo. Proceed? (type YES to continue): " CONFIRM
  if [[ "$CONFIRM" != "YES" ]]; then
    echo "Aborted by user."
    exit 2
  fi
fi

echo "Creating backup directory: $BACKUP_DIR"
mkdir -p "$BACKUP_DIR"

# Find all .git directories (including top-level and nested) and copy them to backup
echo "Backing up all .git directories..."
FOUND=0
while IFS= read -r -d '' gitdir; do
  FOUND=1
  # strip leading ./ if present
  RELPATH="${gitdir#./}"
  DEST_DIR="$BACKUP_DIR/$RELPATH"
  mkdir -p "$(dirname "$DEST_DIR")"
  echo " - backing up $gitdir -> $DEST_DIR"
  cp -a "$gitdir" "$DEST_DIR"
done < <(find . -type d -name .git -print0)

if [[ $FOUND -eq 0 ]]; then
  echo "No .git directories found to back up."
fi

# Remove all .git directories
echo "Removing all .git directories in the tree..."
find . -type d -name .git -prune -exec rm -rf '{}' +

# Remove leftover .gitmodules and modules dir if present
if [[ -f .gitmodules ]]; then
  echo "Removing .gitmodules"
  rm -f .gitmodules
fi
if [[ -d .git/modules ]]; then
  echo "Removing .git/modules"
  rm -rf .git/modules
fi

# Also remove any references in the index (if weird state) by reinitializing
if [[ -d .git ]]; then
  rm -rf .git
fi

# Reinitialize repo
echo "Initializing new git repo (branch: main)..."
git init -b main

# Configure local user if not set (skip if global exists)
if ! git config user.name >/dev/null; then
  # If environment variables are set, use them; otherwise, leave to global
  if [[ -n "${GIT_USER_NAME:-}" ]]; then
    git config user.name "$GIT_USER_NAME"
    git config user.email "${GIT_USER_EMAIL:-you@example.com}"
    echo "Set local git user to: $GIT_USER_NAME / ${GIT_USER_EMAIL:-you@example.com}"
  else
    echo "Using existing global git user (or none). To set local user for this repo, set env GIT_USER_NAME and GIT_USER_EMAIL before running."
  fi
fi

# Ensure nested repos are now just folders (we removed .git inside them)
echo "Staging all files..."
git add .

echo "Committing..."
git commit -m "Initial commit: include all project files (flattened), $TIMESTAMP" || {
  echo "Nothing to commit or commit failed."
}

# Set remote
if git remote | grep -q '^origin$'; then
  git remote remove origin
fi
git remote add origin "$REMOTE"
echo "Remote origin set to $REMOTE"

# Try to push
echo "Pushing to remote origin main..."
if git push -u origin main; then
  echo "Push succeeded."
else
  echo "Push failed. If the remote contains commits you'll need to force push to overwrite history."
  if [[ $FORCE_PUSH -eq 1 ]]; then
    echo "Force pushing to remote (this will overwrite remote history) ..."
    git push -u origin main --force
    echo "Force push done."
  else
    echo "To force push, rerun with --force-push."
    echo "Backup of any previous .git metadata stored at: $BACKUP_DIR"
    exit 3
  fi
fi

echo "Done. Backup of old .git info: $BACKUP_DIR"
echo "If you need to restore nested repo histories, check files inside that backup."

