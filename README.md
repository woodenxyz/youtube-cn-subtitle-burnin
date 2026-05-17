# YouTube Chinese Subtitle Burn-in Skill

This repository contains the `youtube-cn-subtitle-burnin` Agent Skill.

It helps an AI agent turn YouTube videos or local video/subtitle inputs into Simplified Chinese or optional Chinese-English bilingual hard-subtitled MP4 files, while keeping reusable subtitle files, design confirmation frames, and review records.

![YouTube Chinese subtitle skill infographic](assets/youtube-cn-subtitle-skill-infographic.png)

## What It Includes

- `assets/youtube-cn-subtitle-skill-infographic.png` - concise capability overview for the skill
- `youtube-cn-subtitle-burnin/SKILL.md` - the main skill instructions
- `youtube-cn-subtitle-burnin/references/` - workflow, quality gates, review template, and feedback ledger
- `youtube-cn-subtitle-burnin/scripts/` - helper scripts for subtitle cleanup, translation batching, fixed-style Chinese-only and bilingual ASS conversion, bilingual alignment review, cover preview checks, preview creation, burn-in, design confirmation frames, and review
- `dist/youtube-cn-subtitle-burnin.skill` - packaged skill artifact

## Install

Install by copying or unpacking the skill directory into your agent skills folder.

For Daniel's local Do Agent setup:

```bash
mkdir -p /Users/daniel/.agents/skills
rsync -a youtube-cn-subtitle-burnin/ /Users/daniel/.agents/skills/youtube-cn-subtitle-burnin/
```

For Codex-style skill installation, use the skills directory configured by your Codex environment.

## Package

Refresh the packaged artifact after changing files under `youtube-cn-subtitle-burnin/`:

```bash
rm -f dist/youtube-cn-subtitle-burnin.skill
mkdir -p dist
zip -r dist/youtube-cn-subtitle-burnin.skill youtube-cn-subtitle-burnin
```

## Validate

Run these checks before publishing or installing a changed version:

```bash
python3 -m py_compile youtube-cn-subtitle-burnin/scripts/*.py
for f in youtube-cn-subtitle-burnin/scripts/*.py; do python3 "$f" --help >/dev/null || exit 1; done
unzip -l dist/youtube-cn-subtitle-burnin.skill
```

## Workflow Contract

For real video jobs, the skill expects the agent to:

1. keep original source metadata, thumbnail, and description
2. create reusable Chinese SRT and styled ASS subtitle files, plus English SRT and bilingual ASS when bilingual mode is used
3. check source frames for existing burned-in subtitles before choosing bilingual layout
4. keep subtitles on a fixed style profile unless a raised profile is explicitly needed
5. review bilingual Chinese/English timing samples when bilingual mode is used
6. record cover mode and inspect a 320px cover preview when editing covers
7. create a subtitled preview before burning the full video
8. extract design confirmation frames before full burn
9. inspect the final MP4
10. extract review screenshots
11. write a review record
12. record reusable subtitle feedback back into the skill references

Previous MP4, SRT, and ASS outputs should not be overwritten. New versions should use versioned filenames.

## Open Source Notes

This project is released under the MIT License.
