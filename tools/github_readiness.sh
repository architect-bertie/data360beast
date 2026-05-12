#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

fail() {
  printf 'FAIL: %s\n' "$1" >&2
  exit 1
}

warn() {
  printf 'WARN: %s\n' "$1" >&2
}

need() {
  command -v "$1" >/dev/null 2>&1 || fail "Missing required command: $1"
}

need git
need gh

remote_url="$(git remote get-url origin 2>/dev/null || true)"
[[ "$remote_url" == *"github.com/architect-bertie/data360beast"* ]] ||
  fail "origin is not architect-bertie/data360beast: ${remote_url:-<missing>}"

login="$(gh api user --jq '.login' 2>/dev/null || true)"
[[ "$login" == "architect-bertie" ]] ||
  fail "gh API user is not architect-bertie: ${login:-<unavailable>}"

repo="$(gh repo view --json nameWithOwner --jq '.nameWithOwner' 2>/dev/null || true)"
[[ "$repo" == "architect-bertie/data360beast" ]] ||
  fail "gh repo view returned unexpected repo: ${repo:-<unavailable>}"

permission="$(gh repo view --json viewerPermission --jq '.viewerPermission' 2>/dev/null || true)"
case "$permission" in
  ADMIN|MAINTAIN|WRITE) ;;
  *) fail "GitHub permission is not write-capable: ${permission:-<unavailable>}" ;;
esac

default_branch="$(gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name' 2>/dev/null || true)"
[[ -n "$default_branch" ]] || fail "Could not resolve default branch with gh repo view"

git ls-remote --heads origin "$default_branch" >/dev/null 2>&1 ||
  fail "git cannot read origin/$default_branch"

helper="$(git config --global --get-all credential.https://github.com.helper 2>/dev/null || true)"
if [[ "$helper" != *"gh auth git-credential"* ]]; then
  warn "GitHub-specific git credential helper is not gh auth git-credential"
fi

if ! gh auth status >/dev/null 2>&1; then
  warn "gh auth status reported unhealthy, but gh API, repo, permission, and git remote checks passed"
fi

printf 'GitHub readiness OK\n'
printf 'account=%s\n' "$login"
printf 'repo=%s\n' "$repo"
printf 'permission=%s\n' "$permission"
printf 'default_branch=%s\n' "$default_branch"
