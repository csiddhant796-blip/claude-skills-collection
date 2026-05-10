#!/bin/bash
# ============================================================
# Push claude-skills-collection to GitHub
# Usage: bash push_to_github.sh YOUR_GITHUB_TOKEN
# ============================================================

GITHUB_USER="csiddhant796-blip"
REPO_NAME="claude-skills-collection"
TOKEN="${1:-}"

if [ -z "$TOKEN" ]; then
  echo "Usage: bash push_to_github.sh YOUR_GITHUB_TOKEN"
  echo ""
  echo "Get a token at: https://github.com/settings/tokens/new"
  echo "Required scope: repo (full control)"
  exit 1
fi

echo "Creating GitHub repo: $GITHUB_USER/$REPO_NAME ..."
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" \
  -X POST \
  -H "Authorization: token $TOKEN" \
  -H "Content-Type: application/json" \
  https://api.github.com/user/repos \
  -d "{
    \"name\": \"$REPO_NAME\",
    \"description\": \"111+ Claude agent skills for engineering, DevOps, security, ML, databases, and more\",
    \"private\": false,
    \"auto_init\": false
  }")

if [ "$RESPONSE" = "201" ]; then
  echo "✅ Repo created!"
elif [ "$RESPONSE" = "422" ]; then
  echo "ℹ️  Repo already exists, continuing..."
else
  echo "❌ Failed to create repo (HTTP $RESPONSE). Check your token."
  exit 1
fi

echo "Setting remote and pushing..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

git remote remove origin 2>/dev/null || true
git remote add origin "https://$GITHUB_USER:$TOKEN@github.com/$GITHUB_USER/$REPO_NAME.git"
git push -u origin main

echo ""
echo "✅ Done! View your repo at:"
echo "   https://github.com/$GITHUB_USER/$REPO_NAME"
