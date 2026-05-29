# YouTube Chinese Subtitle Skill

[中文](README.md) | English

Turn YouTube videos or local video files into reviewed Chinese-English bilingual MP4 outputs by default, with Chinese above English.

This skill does more than burn text onto a video. It keeps subtitle files, burn-in styling, cover assets, descriptions, preview clips, screenshots, and review notes so each result has a clear review trail.

## Features

- Create Chinese-English bilingual hard-subtitled MP4 outputs by default
- Create Chinese-only hard-subtitled MP4 outputs when explicitly requested
- Translate subtitles and descriptions with the current agent model by default, with a config option for local Local Translate
- Download and retain the original YouTube thumbnail by default; do not edit the cover by default
- Keep reusable SRT and ASS subtitle files
- Create a subtitled preview before processing the full video
- Check subtitle size, position, segmentation, overlap, and phone-size readability
- Optionally retain and prepare YouTube covers and descriptions
- Output screenshots and review notes for final checking

## Installation

Recommended one-command install:

```bash
npx skills add woodenxyz/youtube-cn-subtitle-burnin
```

Restart your agent app after installation, then ask it to use `youtube-cn-subtitle-burnin` for a video task.

### Manual Install

If your environment cannot use `npx skills add`, install the packaged skill into a shared skills directory:

```bash
git clone https://github.com/woodenxyz/youtube-cn-subtitle-burnin.git
cd youtube-cn-subtitle-burnin
mkdir -p ~/.agents/skills
unzip -o dist/youtube-cn-subtitle-burnin.skill -d ~/.agents/skills
```

### Install for Codex only

If you only want Codex to discover the skill, install it into Codex's own skills directory.

```bash
git clone https://github.com/woodenxyz/youtube-cn-subtitle-burnin.git
cd youtube-cn-subtitle-burnin
mkdir -p ~/.codex/skills
unzip -o dist/youtube-cn-subtitle-burnin.skill -d ~/.codex/skills
```

## Usage Examples

```text
Use youtube-cn-subtitle-burnin to create a Chinese-English bilingual version of this YouTube video.
Keep the SRT and ASS files. For the cover, add only “中文字幕” and the source label; do not translate the original cover text.
```

```text
Use youtube-cn-subtitle-burnin to create a Chinese-only hard-subtitled version.
Do not add the English reference line. Keep the MP4, SRT, ASS, and review screenshots.
```

## What You Provide

- A YouTube URL, or a local video file
- Whether to override the default bilingual mode, for example by explicitly asking for Chinese-only
- Whether to override the default agent translation provider, for example by asking for the local model
- Whether the cover should be prepared
- Optional glossary, product names, or translation preferences

## What You Get

- Hard-subtitled MP4
- Chinese SRT
- Styled ASS used for burn-in
- English SRT and bilingual ASS when bilingual mode is used
- Original cover; edited cover and 320px thumbnail preview when cover work is requested
- Original and Chinese descriptions
- Preview clip, design frames, final screenshots, and review notes

## Default Config

Default settings live in `youtube-cn-subtitle-burnin/config/defaults.json`:

```json
{
  "translation_provider": "agent",
  "subtitle_mode": "bilingual",
  "download_thumbnail": true,
  "cover_edit": "not_requested",
  "cover_mode": "none"
}
```

In practice, the skill defaults to agent translation, bilingual subtitles, original thumbnail download, and no cover editing unless requested.

## Good Use Cases

- Turning English YouTube technical videos into Chinese study copies
- Adding Chinese subtitles to courses, interviews, or product walkthroughs
- Creating bilingual versions with a smaller English reference line
- Keeping subtitle source files instead of only the burned MP4
- Requiring preview and screenshot checks before accepting a result

## Quality Gates

Every real output should pass these checks:

- The preview clip visibly contains subtitles.
- Subtitles are readable at phone size.
- Subtitle styling matches the fixed profile.
- Bilingual subtitles include sampled checks across Chinese, English, and speech timing.
- Edited covers remain readable as 320px thumbnail previews.
- The final MP4 has valid audio, video, screenshots, and delivery files.

## Requirements

- Python 3
- ffmpeg / ffprobe
- yt-dlp
- Pillow
- An agent model that can run the skill and handle translation, workflow control, judgment, repair, and review
- For local translation only: installed Local Translate skill and a working local Ollama translation model

## Maintenance

Refresh the packaged artifact after changing files under `youtube-cn-subtitle-burnin/`:

```bash
rm -f dist/youtube-cn-subtitle-burnin.skill
mkdir -p dist
zip -r dist/youtube-cn-subtitle-burnin.skill youtube-cn-subtitle-burnin
```

Run these checks before publishing or installing a changed version:

```bash
python3 -m py_compile youtube-cn-subtitle-burnin/scripts/*.py
for f in youtube-cn-subtitle-burnin/scripts/*.py; do python3 "$f" --help >/dev/null || exit 1; done
unzip -l dist/youtube-cn-subtitle-burnin.skill
```

## Workflow Overview

<img src="assets/youtube-cn-subtitle-skill-infographic.png" alt="YouTube Chinese subtitle skill infographic" width="560">

## License

MIT
