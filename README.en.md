# YouTube Chinese Subtitle Skill

[中文](README.md) | English

Turn YouTube videos or local video files into reviewed Chinese-subtitled MP4 outputs.

This skill does more than burn text onto a video. It keeps reusable subtitle files, subtitle styling, cover previews, descriptions, screenshots, and review notes so the result can be checked, revised, and reused later.

## Install

Copy or unpack the skill directory into your agent skills folder.

For Daniel's local Do Agent setup:

```bash
mkdir -p /Users/daniel/.agents/skills
rsync -a youtube-cn-subtitle-burnin/ /Users/daniel/.agents/skills/youtube-cn-subtitle-burnin/
```

For Codex-style environments, use the skills directory configured by your Codex setup.

After installation, ask the agent to use `youtube-cn-subtitle-burnin` for video subtitle jobs.

## Usage Examples

```text
Use youtube-cn-subtitle-burnin to create a Chinese-subtitled version of this YouTube video.
Keep the SRT and ASS files. For the cover, add only “中文字幕” and the source label; do not translate the original cover text.
```

For bilingual output:

```text
Use youtube-cn-subtitle-burnin to create a Chinese-English hard-subtitled version.
Chinese should be the main subtitle; English should be a smaller reference line. Keep the MP4, SRT, ASS, and review screenshots.
```

## What You Provide

- A YouTube URL, or a local video file
- Whether the output should be Chinese-only or bilingual
- Whether the cover should be processed
- Optional glossary, product names, or translation preferences

## What You Get

- Hard-subtitled MP4
- Chinese SRT
- Styled ASS used for burn-in
- English SRT and bilingual ASS when bilingual mode is used
- Original cover, edited cover, and 320px thumbnail preview
- Original and Chinese descriptions
- Preview clip, design frames, final screenshots, and review notes

## Who It Is For

- You want a Chinese study copy of an English YouTube technical video.
- You need Chinese-only or Chinese-English subtitles for courses, interviews, or product walkthroughs.
- You want a repeatable subtitle workflow instead of adjusting styles by hand for every video.
- You want to keep SRT / ASS files, not only the final burned MP4.

## What It Solves

- Unstable subtitle styling: fixed profiles for Chinese-only and bilingual subtitles
- Weak bilingual correspondence: sampled checks for Chinese, English, and speech timing
- Messy automatic captions: cleanup for overlaps, empty cues, broken segments, and dangling endings
- Inconsistent cover handling: three explicit modes for preserving, translating, or localizing cover copy
- Non-reusable delivery: SRT, ASS, screenshots, and review notes are retained by default

## Quality Gates

Every real video output should pass these checks:

- The preview clip must visibly contain subtitles.
- Subtitles must be readable at phone size.
- Subtitle styling must match a fixed profile.
- Bilingual subtitles must include alignment samples.
- Edited covers must be checked as 320px thumbnail previews.
- The final MP4 must have valid audio, video, screenshots, and delivery files.

## Requirements

- Python
- ffmpeg / ffprobe
- yt-dlp
- Pillow
- An agent model that can run the skill and handle translation, judgment, and review

## Maintainer Notes

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

This project is released under the MIT License.
