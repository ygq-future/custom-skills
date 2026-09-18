# no-negative-echo

An Agent Skill that removes conversational correction residue from durable project language.

## Structure

```text
no-negative-echo/
├── SKILL.md
├── README.md
├── evals/
│   └── evals.json
├── references/
│   └── examples.md
└── scripts/
    └── scan_echo.py
```

`SKILL.md` is the required Agent Skills entry point. The remaining files are optional supporting resources used through progressive disclosure.

## Install

Copy the entire `no-negative-echo` directory into the skills directory used by your Agent/skills manager. Keep the directory name and the `name:` field in `SKILL.md` identical.

## Optional literal scan

```bash
python scripts/scan_echo.py --forbidden "service approach" --forbidden "legacy dialog" path/to/repo
```

A match is only a review candidate. The skill's semantic rules decide whether the wording is actually residue or legitimate history/domain language.
