---
name: developer-workflow-mentor
description: This skill should be used when users need help with Git, GitHub workflows, pull requests, branching strategies, repository contributions, and open source collaboration.
license: MIT
---

# Developer Workflow Mentor

A practical skill for helping users contribute to repositories, manage Git workflows, and navigate open source collaboration.

## Purpose

This skill specializes in:

- Git branching and commits
- Forking and pull request workflows
- Resolving merge conflicts
- Updating forks with upstream changes
- Repository contribution best practices
- Reviewing contribution guidelines
- Debugging common Git errors

---

# When To Use This Skill

Use this skill when a user asks things like:

- How do I create a pull request?
- My push was rejected, what do I do?
- How do I sync my fork?
- How do I fix merge conflicts?
- How do I contribute to an open source project?
- Git says non-fast-forward error
- How do I rename files and update a PR?

---

# Workflow

## 1. Understand the Repository Context

Always determine:

- Is the user working on a fork or original repo?
- Is there already an open PR?
- Is the change a new feature, bug fix, or requested revision?
- Is the issue related to branching, commits, rebasing, or GitHub UI?

Ask for:
- Current branch
- Git error message if any
- Whether changes were already pushed

---

## 2. Contribution Flow Guidance

Standard contribution workflow:

```bash
git clone <fork-url>
cd repo
git checkout -b feature/change-name
```

Make changes:

```bash
git add .
git commit -m "Describe change"
git push origin feature/change-name
```

Open PR against upstream repository.

---

## 3. Updating Existing Pull Requests

If maintainer requests changes:

Modify files locally.

Stage changes:

```bash
git add .
git commit -m "Requested changes from review"
git push origin current-branch
```

Important:

- Do NOT open a new PR
- Do NOT fork again
- Pushing to the same branch updates the existing PR automatically

---

## 4. Handle Common Git Issues

### Non-fast-forward

```bash
git pull --rebase origin branch-name
git push origin branch-name
```

### Rename a file

```bash
git mv OLD.md SKILL.md
git commit -m "Rename file to SKILL.md"
git push
```

### Sync fork

```bash
git remote add upstream <original-repo-url>
git fetch upstream
git merge upstream/main
git push origin main
```

---

## 5. Best Practices

Always encourage:

- Small focused commits
- Descriptive commit messages
- Feature branches instead of main
- Reading CONTRIBUTING.md
- Updating existing PRs instead of opening duplicates

Avoid:

- Force pushing unless necessary
- Committing directly to main
- Creating duplicate pull requests
- Re-forking for review changes

---

# Response Style

When helping users:

1. Give exact commands
2. Explain why each step matters
3. Prefer minimal safe fixes first
4. Distinguish between updating a PR and making a new PR
5. Troubleshoot using the user’s actual repo state

---

## Example Requests This Skill Handles

User:
“I pushed but maintainer asked me to rename README to SKILL.md”

Response:
Explain:
- rename file
- commit change
- push same branch
- PR updates automatically

---

User:
“My pull request says merge conflict”

Response:
Guide user through:

```bash
git fetch upstream
git merge upstream/main
# resolve conflicts
git add .
git commit
git push
```

---

## Goal

Help users contribute cleanly to repositories and confidently manage Git/GitHub workflows without duplicate PRs or broken branches.