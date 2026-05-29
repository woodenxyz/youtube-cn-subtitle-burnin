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
| 2026-05-16 | translation workflow | The active agent should translate subtitles instead of defaulting to external APIs/tools | The workflow treated translation as an external automation task first | yes | Make current agent-model translation the default path; APIs/tools are fallback only |
| 2026-05-16 | readability | Subtitle line breaks sometimes split Chinese or English phrases awkwardly | ASS generation wrapped by raw length instead of semantic boundaries | yes | Add semantic wrapping and line-break checks for protected terms and meaning chunks |
| 2026-05-16 | source fallback | YouTube Chinese captions can be rate-limited | Repeated timedtext requests returned HTTP 429 | yes | Stop repeated retries, use English captions, translate through the configured provider, and record source limitation |
| 2026-05-16 | tooling | Default ffmpeg may lack subtitle burn filters | Local ffmpeg lacked ass/subtitles/drawtext filters | yes | Check subtitle burn support before full burn and switch to a libass-capable ffmpeg build |
| 2026-05-16 | cover | Video thumbnail should be retained and user should be asked whether it needs translation | The subtitle workflow focused on MP4/SRT/ASS and did not define cover handling | yes | Download thumbnail during source acquisition; ask and record cover translation preference |
| 2026-05-16 | cover | Add “中文字幕” and YouTube-style author information to the cover when requested | Cover translation needed a concrete output mode, not only a yes/no preference | yes | Add Cover Processing Mode with placement, preservation, versioned output, and visual check rules |
| 2026-05-16 | description | Video description should be downloaded and translated to Chinese when needed | Workflow retained video/subtitle/cover files but did not define description handling | yes | Extract original description, translate non-Chinese descriptions with the configured provider, and preserve proper nouns, URLs, and timestamps |
| 2026-05-16 | model portability | Skill should work with non-GPT agent models such as Minimax when the agent can run the local workflow | Translation instructions were worded around Codex/GPT as the default model | yes | Use model-neutral workflow wording; keep old Codex batch script as a compatibility alias and agent-model batches as fallback only |
| 2026-05-16 | bilingual layout | Bilingual subtitles can become too tall or duplicate burned-in English subtitles | Chinese-only layout rules were reused without checking source subtitles or total subtitle height | yes | Add optional bilingual ASS generation, source subtitle check frames, and design confirmation frames before full burn |
| 2026-05-16 | bilingual layout | Bilingual subtitle video showed stray `N` characters and Chinese/English lines felt mismatched | ASS newline escaping leaked into visible text, and semantic Chinese screens were paired with fragmented rolling English captions | yes | Add visible newline artifact gate and require matched cue boundaries when semantic Chinese plus rolling English looks messy |
| 2026-05-16 | bilingual layout | Bilingual subtitles looked messier than Chinese-only | English was treated as an equally prominent second subtitle and exact matching could fragment the Chinese reading rhythm | yes | Default bilingual mode to Chinese-primary / English-auxiliary, smaller English, first-minute visual check, and matched-boundary preview only when it keeps Chinese readable |
| 2026-05-17 | style | Subtitle style varied across recent video jobs | Font size, outline, and vertical placement were still partly chosen per job instead of fixed by profile | yes | Add fixed subtitle style profiles and `check_subtitle_style.py`; record style profile in reviews |
| 2026-05-17 | bilingual alignment | Chinese/English correspondence and voice timing still needed manual repair | Quality gates checked layout and overlap, but did not require representative meaning-and-timing samples | yes | Add `check_bilingual_alignment.py` and require bilingual alignment reports before final burn |
| 2026-05-17 | cover | Cover translation/rewrite behavior and added-label style varied across jobs | Cover workflow lacked explicit modes and thumbnail-size preview checks | yes | Add cover modes, fixed label treatment, and 320px preview gate |
| 2026-05-23 | description | Description document in `08-description/` was left untranslated | The workflow mentioned description translation, but it was too easy to miss during final delivery | yes | Make the Chinese description file a hard delivery gate and translate it with the configured provider |
| 2026-05-24 | bilingual default | User had to repeatedly ask for Chinese above English bilingual subtitles | The workflow still treated bilingual output as optional instead of the default mode | yes | Make bilingual output the default, record subtitle mode reason, and require Chinese-only exceptions to be explicit |
| 2026-05-24 | size | User felt the current subtitle size was a bit small and asked to compare against Bilibili references from 影视飓风 and MrBeast官方账号 | The Chinese line was close to reference scale, but the ASS bilingual English auxiliary line was too small compared with MrBeast-style bilingual captions | yes | Raise the fixed bilingual profile to v2, with a slightly larger Chinese line and a clearer English auxiliary line; add reference-scale checks before full burn |
| 2026-05-29 | translation workflow | User initially wanted subtitle and description translation to use the local Local Translate capability instead of the agent model to save tokens and control quality | The workflow still made the current agent model the default bulk translator | yes | Superseded by later same-day feedback below: keep Local Translate available, but no longer as the default |
| 2026-05-29 | translation quality | User found the agent model translates better than the local model and wants a configurable choice | The workflow had hard-switched the default to Local Translate instead of keeping provider choice explicit | yes | Add `config/defaults.json`; set `translation_provider: agent`, `subtitle_mode: bilingual`, `download_thumbnail: true`, `cover_edit: not_requested`, and keep Local Translate as `translation_provider: local` |

## Entries
