# 🛠️ Anthropic Skill Creator Resources

## Purpose
- Guide for creating effective skills
- Help package specialized knowledge, workflows, and tool integrations
- Turn Claude into a more domain-specific assistant through reusable skill design

## What a Skill Includes
- `SKILL.md` (required)
- YAML frontmatter with:
  - `name`
  - `description`
- Optional bundled resources:
  - `scripts/`
  - `references/`
  - `assets/`

## What Skills Provide
- Specialized workflows
- Tool integrations
- Domain expertise
- Bundled reusable resources

## Skill Structure
```text
skill-name/
├── SKILL.md
├── scripts/
├── references/
└── assets/
```

## Bundled Resources
### Scripts
- Store executable code for repeated or deterministic tasks
- Example: PDF rotation or other utility scripts

### References
- Store documentation, schemas, policies, and domain knowledge
- Load only when needed to keep the main skill lean

### Assets
- Store templates, images, icons, fonts, boilerplate, and other output resources
- Use in outputs without needing to load them into context

## Core Design Principle
- Use progressive disclosure:
  - Metadata always available
  - `SKILL.md` body loaded when the skill triggers
  - Bundled resources loaded only when needed

## Skill Creation Process
1. Understand the skill with concrete examples
2. Plan reusable contents
3. Initialize the skill
4. Edit the skill
5. Package the skill
6. Iterate and improve

## Initialization
- Use:
```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

## Packaging
- Use:
```bash
scripts/package_skill.py <path/to/skill-folder>
```
- Optional output directory:
```bash
scripts/package_skill.py <path/to/skill-folder> ./dist
```

## Best Practices
- Write metadata clearly and specifically
- Use third-person phrasing in the description
- Write instructions in imperative form
- Keep `SKILL.md` lean
- Move detailed documentation to `references/`
- Avoid duplicating the same information across files

## Validation Checks During Packaging
- YAML frontmatter is valid
- Required fields are present
- Naming and structure are correct
- Description quality is acceptable
- Resource organization is proper

## Example Use Cases
- Image editor skill
- PDF editor skill
- Frontend webapp builder
- BigQuery helper
- Brand guidelines skill
