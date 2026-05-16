# AGENTS.md

This project stores the source and packaged artifact for the `youtube-cn-subtitle-burnin` Codex skill.

## Project Scope

- Source skill directory: `youtube-cn-subtitle-burnin/`
- Packaged skill artifact: `dist/youtube-cn-subtitle-burnin.skill`
- Purpose: turn YouTube videos or local video/subtitle inputs into Simplified Chinese hard-subtitled MP4 outputs, with retained subtitle files, review screenshots, and review notes.

## Working Rules

- Keep changes narrowly focused on this skill. Do not reorganize the surrounding PARA repository.
- Treat subtitle work as a QA workflow, not only translation.
- Before producing or accepting a video result, read:
  - `youtube-cn-subtitle-burnin/references/workflow.md`
  - `youtube-cn-subtitle-burnin/references/quality-gates.md`
  - `youtube-cn-subtitle-burnin/references/review-template.md`
- When user feedback reports a reusable subtitle issue, also read and update:
  - `youtube-cn-subtitle-burnin/references/feedback-ledger.md`

## Validation

When changing skill files or scripts, run the relevant checks before reporting completion:

```bash
python3 -m py_compile youtube-cn-subtitle-burnin/scripts/*.py
for f in youtube-cn-subtitle-burnin/scripts/*.py; do python3 "$f" --help >/dev/null || exit 1; done
unzip -l dist/youtube-cn-subtitle-burnin.skill
```

For actual video jobs, follow the skill workflow:

- check subtitle timing and text quality
- make a subtitled preview before full burn
- inspect the final MP4
- extract review screenshots
- fill the review record

Do not overwrite previous MP4, SRT, or ASS outputs; create a new version instead.

## Packaging Rule

If files under `youtube-cn-subtitle-burnin/` change, refresh `dist/youtube-cn-subtitle-burnin.skill` before considering the skill updated.
