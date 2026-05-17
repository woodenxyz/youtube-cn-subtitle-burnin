# YouTube Chinese Subtitle Skill

[中文](README.md) | English

Turn YouTube videos or local video files into reviewed Chinese-subtitled MP4 outputs that can be checked, revised, and reused.

This skill does more than burn text onto a video. It keeps subtitle files, burn-in styling, cover assets, descriptions, preview clips, screenshots, and review notes so each result has a clear review trail.

## Features

- Create hard-subtitled Chinese MP4 outputs
- Optionally create Chinese-English bilingual hard-subtitled MP4 outputs
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
Use youtube-cn-subtitle-burnin to create a Chinese-subtitled version of this YouTube video.
Keep the SRT and ASS files. For the cover, add only “中文字幕” and the source label; do not translate the original cover text.
```

```text
Use youtube-cn-subtitle-burnin to create a Chinese-English hard-subtitled version.
Chinese should be the main subtitle; English should be a smaller reference line. Keep the MP4, SRT, ASS, and review screenshots.
```

## What You Provide

- A YouTube URL, or a local video file
- Whether the output should be Chinese-only or bilingual
- Whether the cover should be prepared
- Optional glossary, product names, or translation preferences

## What You Get

- Hard-subtitled MP4
- Chinese SRT
- Styled ASS used for burn-in
- English SRT and bilingual ASS when bilingual mode is used
- Original cover, edited cover, and 320px thumbnail preview
- Original and Chinese descriptions
- Preview clip, design frames, final screenshots, and review notes

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
- An agent model that can run the skill and handle translation, judgment, and review

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
