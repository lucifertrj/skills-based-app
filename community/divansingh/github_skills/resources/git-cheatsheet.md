# Git Cheat Sheet

## Branching

Create branch

```bash
git checkout -b feature-name
```

Switch branch

```bash
git checkout branch-name
```

List branches

```bash
git branch
```

---

## Staging and Commits

Stage all files

```bash
git add .
```

Commit

```bash
git commit -m "Meaningful commit message"
```

View history

```bash
git log --oneline
```

---

## Push

Push branch

```bash
git push origin branch-name
```

Set upstream first push

```bash
git push -u origin branch-name
```

---

## Pull and Sync

Pull latest

```bash
git pull
```

Rebase latest changes

```bash
git pull --rebase origin main
```

Sync fork

```bash
git fetch upstream
git merge upstream/main
```

---

## Rename Files

```bash
git mv README.md SKILL.md
git commit -m "Rename file"
git push
```