# Quality Gates

Use this file before accepting a subtitle or video output. A failed gate blocks delivery unless the user explicitly accepts the limitation.

## Automatic Gates

- No subtitle time overlap.
- No empty subtitle text.
- No accidental duplicate active subtitles in ASS.
- No short flashes below the chosen threshold unless they are intentional one-word reactions.
- No screen ending with dangling connectors or incomplete predicates.
- No screen ending with punctuation that leaves the sentence visibly unfinished, such as `，`、`、`、`：`、`；`.
- No screen remains too long or visually dense after dangling-ending repair.
- No line break splitting product names, English phrases, code/commands, number-unit pairs, or common Chinese meaning chunks.
- MP4 has valid duration, video stream, audio stream, and expected resolution.
- ffmpeg subtitle burn support is checked before full burn; if native subtitle filters are unavailable, the reusable PIL fallback renderer is used and recorded.
- A subtitled preview clip exists before full burn.
- The preview clip contains at least one visible subtitle cue; if the selected one-minute range has no subtitles, the preview duration or window is adjusted.
- Review screenshots can be extracted from the final MP4.
- Original YouTube description is extracted and retained.
- If the original description is not Chinese, a Chinese translated description is retained.
- Original video thumbnail is downloaded and retained.
- Cover edit preference is recorded before delivery.
- If cover editing/localization is requested, edited cover exists in `07-cover/` and the original thumbnail remains unchanged.
- Edited cover preserves all original thumbnail text exactly as-is unless the user explicitly requested text translation or redesign.
- Edited cover includes `中文字幕` and YouTube author/source information.

## Visual Gates

- Subtitle must be readable on phone-sized playback, not just desktop.
- Text must be strong enough against bright and dark backgrounds.
- Font size, outline, vertical position, and line breaks must be approved from preview screenshots before full burn.
- Full video generation must wait for user approval of the subtitled preview clip unless the user explicitly waives this step or asks the agent to handle the job end to end. In direct-completion mode, preview screenshots must be self-checked and recorded.
- Subtitle must not cover faces, code, chart labels, important product UI, or bottom controls.
- If the video is a software tutorial, inspect bottom input boxes, status bars, and right-side presenter overlays.
- Edited cover text must be readable at thumbnail size and must not cover faces, important UI, product signals, or the original main title.

## Language Gates

- Meaning is faithful to the original.
- Chinese is natural and watchable.
- Technical terms and names are consistent.
- Description translation preserves proper nouns, product names, URLs, and chapter timestamps.
- Negation, numbers, time, conditions, and confidence level are preserved.
- Long English sentences are converted into readable Chinese semantic screens.
- Subtitle line breaks preserve readable Chinese and keep protected terms intact.

## Known Reusable Failures

| Issue | Failure signal | Preventive action |
|---|---|---|
| YouTube overlap | Multiple cues active at once; previous line remains onscreen | Run overlap check before ASS generation and repair to non-overlap timing |
| Too fragmented | Frequent one-second flashes; reading feels jumpy | Merge related cues into semantic screens |
| Half-sentence screens | Screen ends with connector or unfinished predicate | Rebuild screens around complete sentences or closed meaning blocks |
| Incomplete punctuation screens | Screen ends with `，`、`、`、`：`、`；` even though the thought continues | Merge with the following cue or split again at a complete semantic boundary |
| Long dense screens after repair | Dangling-ending repair passes, but a subtitle still holds too much text or stays too long | Split long repaired cues by Chinese semantic punctuation and re-check readability |
| Subtitle too small | Looks acceptable on desktop but tiring on phone-sized playback | Require preview screenshots and adjust size/outline before full burn |
| Preview without subtitles | One-minute preview shows no subtitle, so user cannot judge style | Extend duration or move preview to a subtitle-bearing window before asking for approval |
| Bottom UI occlusion | Subtitle covers input fields, controls, code, chart labels, or lower-third text | Move subtitle upward, reduce line count, or use a safer region for that segment |
| YouTube translated caption rate limit | Chinese timedtext download returns HTTP 429 or repeated subtitle download errors | Stop repeated retries, use English captions, translate with Codex, and record the source limitation |
| External translation detour | Workflow tries APIs/tools even though current Codex can translate | Use current Codex as the default translator; external APIs/tools are fallback only |
| Translation batch drift | Long video translation misses ids, reorders subtitles, or cannot resume after interruption | Use numbered JSON batches, verify all ids, and save cache after every batch |
| Unstable cue ids | Cleaned captions are resegmented, then translation cache is matched against position-only ids | Keep stable `id` values in cue JSON and use those ids for batching/cache application |
| Hard character wrapping | Line break cuts product names, English phrases, or Chinese meaning chunks | Generate ASS with semantic wrapping and check line breaks from preview frames |
| Missing ffmpeg subtitle support | Full burn fails because ffmpeg lacks ass/subtitles filters | Run ffmpeg subtitle support check before preview/full burn and switch to a libass-capable build |
| One-off fallback renderer | Project contains a temporary burn-in script that is not reusable next time | Use `scripts/burn_subtitles_pil.py` for fallback hard subtitles and keep renderer changes in the skill |
| Missing thumbnail | Video is delivered without saving the YouTube cover | Download and retain the thumbnail during source acquisition |
| Missing description | Video is delivered without saving the YouTube description | Extract and retain the original description during source acquisition |
| Description translation loses names | Chinese description translates product names, URLs, or timestamps incorrectly | Preserve proper nouns, product names, URLs, and chapter timestamps while translating surrounding text |
| Unclear cover preference | User may expect a Chinese-subtitle cover but the workflow never asks | Ask whether the thumbnail/cover should be prepared during intake and record the answer |
| Original cover text changed | Existing thumbnail wording is translated, rewritten, erased, or replaced without explicit user request | Keep original cover text unchanged; add only `中文字幕` and author/source information |
| Missing cover author | Edited cover only adds `中文字幕` and omits the YouTube author/source | Add compact author/source text such as `作者：<channel>` or `<channel> · @handle` |
| Cover text blocks key image | Added Chinese label or author text covers a face, product signal, or title | Place cover text in empty space, use compact YouTube-style labels, and visually inspect before delivery |
| Edited cover not retained | Cover was generated but not copied into the project outputs | Copy edited cover into `07-cover/` with a versioned filename and keep the generator original in place |
| Accidental overwrite | Re-running a script replaces a previous MP4/SRT/ASS output | Choose a new versioned filename; only use force overwrite for scratch tests |

## Adding New Gates

When user feedback is reusable across future videos, add a new row above with:

- issue name
- failure signal
- preventive action

Then add the corresponding workflow step to `workflow.md`.
