# Pull Request Guide

## Standard Workflow

1 Fork repository

2 Clone your fork

```bash
git clone <fork-url>
cd repo
```

3 Create feature branch

```bash
git checkout -b feature/update
```

4 Make changes

5 Commit

```bash
git add .
git commit -m "Update contribution"
```

6 Push

```bash
git push origin feature/update
```

7 Open Pull Request

---

## Updating Existing PR

Do not create another PR.

Make requested changes:

```bash
git add .
git commit -m "Address review feedback"
git push
```

Existing PR updates automatically.

---

## Before Opening PR

Checklist:

- Files correctly named
- No unnecessary files
- Follows repository guidelines
- Clear commit messages
- PR description added