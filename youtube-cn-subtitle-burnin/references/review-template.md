# Review Template

Copy this structure into each video's `06-review/review.md`.

```text
# Review

Video:
URL:
Channel:
Duration:
Use:

Source subtitle:
Source subtitle state:
Original description:
Chinese description:
Original thumbnail:
Edited cover:
Subtitle mode:
English SRT:
Chinese SRT:
ASS:
Preview MP4:
Design confirmation frames:
Burned MP4:
Review screenshots:
Delivery files:

## Checks

- [ ] Subtitle overlap check passed
- [ ] Empty subtitle check passed
- [ ] Dangling ending check passed
- [ ] Incomplete punctuation ending check passed
- [ ] Bad line-break check passed
- [ ] Source-video subtitle check frames extracted
- [ ] Source subtitle state recorded
- [ ] Subtitle mode recorded
- [ ] Final Chinese SRT retained for delivery
- [ ] Final English SRT retained when bilingual mode is used
- [ ] Final ASS retained for delivery
- [ ] Bilingual layout check passed when bilingual mode is used
- [ ] ffmpeg subtitle burn support checked
- [ ] Subtitle burn method recorded, including PIL fallback if used
- [ ] Original YouTube description extracted and retained
- [ ] Chinese description retained when original is not Chinese
- [ ] Description translation preserves product names, URLs, and timestamps
- [ ] Original thumbnail downloaded and retained
- [ ] Cover edit preference recorded
- [ ] Edited cover retained when requested
- [ ] Edited cover preserves original cover text
- [ ] Edited cover includes `中文字幕`
- [ ] Edited cover includes YouTube author/source information
- [ ] Edited cover visually checked when requested
- [ ] Video stream/audio stream check passed
- [ ] Subtitled preview clip generated before full burn
- [ ] Preview clip visibly contains subtitles
- [ ] Design confirmation frames extracted before full burn
- [ ] Design confirmation frames show acceptable size, line count, position, and occlusion
- [ ] Bilingual design frames show Chinese above English when bilingual mode is used
- [ ] User approved preview readability before full burn
- [ ] Preview readability self-checked when direct-completion mode applies
- [ ] First minute checked
- [ ] Midpoint checked
- [ ] Final minute checked
- [ ] Dense UI/code/diagram area checked
- [ ] User-reported timestamps checked
- [ ] Versioned output filenames used; no prior MP4/SRT/ASS overwritten

## Findings

| Time | Observation | Result |
|---|---|---|

## Changes

| Version | Change | Reason |
|---|---|---|

## Decision

Deliverable status: pass / pass with known limits / blocked
Known limits:
Next action:
```
