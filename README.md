# Custom Skills

A collection of personal and customized agent skills for coding agents (Claude Code, Codex, OMP, etc.), managed via [Skills Manager](https://github.com/xingkongliang/skills-manager).

## Available Skills

| Skill | Description |
| :--- | :--- |
| [`project-quality`](./project-quality) | Establish, audit, and maintain a cross-stack quality system with compiler diagnostics and unified Quality Gate. |
| [`no-negative-echo`](./no-negative-echo) | Prevent rejected, superseded, or corrected ideas from leaking into final-facing project history and language. |

## Installation

### Via Skills Manager

Install an individual skill directly using its Git subpath:

```bash
skills-manager-cli skills install https://github.com/ygq-future/custom-skills/tree/main/project-quality
skills-manager-cli skills install https://github.com/ygq-future/custom-skills/tree/main/no-negative-echo
```
