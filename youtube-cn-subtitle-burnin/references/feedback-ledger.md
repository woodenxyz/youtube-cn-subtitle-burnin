# Feedback Ledger

Record user-reported subtitle problems here. Reusable issues must also update `quality-gates.md` and `workflow.md`.

## Entry Template

```text
Date:
Video/output:
Timestamp:
Category: translation / segmentation / timing / hold-duration / size / occlusion / terminology / readability
User issue:
Confirmed cause:
Fix applied:
Reusable: yes / no
SOP update:
Quality gate update:
```

## Seeded Lessons

| Date | Category | User issue | Confirmed cause | Reusable | SOP/gate update |
|---|---|---|---|---|---|
| 2026-05-10 | timing | Double-line alternation and previous sentence residue | YouTube automatic captions used overlapping rolling cues | yes | Always run overlap check before ASS generation |
| 2026-05-10 | hold-duration | Subtitles changed too quickly | Non-overlap timing preserved overly fragmented cue boundaries | yes | Merge related cues into semantic screens |
| 2026-05-10 | segmentation | A screen showed an incomplete sentence | Mechanical merging split a complete idea across screens | yes | Build screens around complete sentences or closed meaning blocks |
| 2026-05-12 | size | Final video subtitles were too small and not obvious enough | Style was accepted without phone-readable visual confirmation | yes | Require preview screenshots and style approval before full burn |
| 2026-05-16 | translation workflow | Codex itself should translate subtitles instead of defaulting to external APIs/tools | The workflow treated translation as an external automation task first | yes | Make current Codex self-translation the default path; APIs/tools are fallback only |
| 2026-05-16 | readability | Subtitle line breaks sometimes split Chinese or English phrases awkwardly | ASS generation wrapped by raw length instead of semantic boundaries | yes | Add semantic wrapping and line-break checks for protected terms and meaning chunks |
| 2026-05-16 | source fallback | YouTube Chinese captions can be rate-limited | Repeated timedtext requests returned HTTP 429 | yes | Stop repeated retries, use English captions, translate with Codex, and record source limitation |
| 2026-05-16 | tooling | Default ffmpeg may lack subtitle burn filters | Local ffmpeg lacked ass/subtitles/drawtext filters | yes | Check subtitle burn support before full burn and switch to a libass-capable ffmpeg build |
| 2026-05-16 | cover | Video thumbnail should be retained and user should be asked whether it needs translation | The subtitle workflow focused on MP4/SRT/ASS and did not define cover handling | yes | Download thumbnail during source acquisition; ask and record cover translation preference |
| 2026-05-16 | cover | Add “中文字幕” and YouTube-style author information to the cover when requested | Cover translation needed a concrete output mode, not only a yes/no preference | yes | Add Cover Processing Mode with placement, preservation, versioned output, and visual check rules |
| 2026-05-16 | description | Video description should be downloaded and translated to Chinese when needed | Workflow retained video/subtitle/cover files but did not define description handling | yes | Extract original description, translate non-Chinese descriptions with Codex, and preserve proper nouns, URLs, and timestamps |

## Entries
