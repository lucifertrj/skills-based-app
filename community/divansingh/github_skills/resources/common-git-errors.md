# Common Git Errors

## Non-fast-forward

Error:

```bash
failed to push some refs
```

Fix:

```bash
git pull --rebase origin main
git push
```

---

## Merge Conflict

Fix:

```bash
git fetch upstream
git merge upstream/main
```

Resolve conflict markers manually:

```text
<<<<<<<
=======
>>>>>>>
```

Then:

```bash
git add .
git commit
git push
```

---

## Detached HEAD

Create branch from current work:

```bash
git checkout -b rescue-branch
```

---

## Permission Denied on Push

Likely pushing to original repo.

Push to your fork:

```bash
git push origin branch-name
```

---

## Wrong File Name

Rename:

```bash
git mv oldname.md SKILL.md
git commit -m "Rename file"
git push
```