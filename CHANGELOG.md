# Changelog

## Unreleased

- Synced the project source from the installed Do Agent skill version.
- Added the expanded YouTube subtitle workflow helpers.
- Prepared repository-level files for standalone GitHub publishing.
- Added fixed subtitle style profiles, bilingual alignment review, and cover mode/320px preview gates.
- Made the Chinese YouTube description file a required delivery gate for non-Chinese descriptions.
- Made Chinese-English bilingual subtitles the default output mode: Chinese above English, with Chinese-only limited to explicit requests or source-video exceptions.
- Removed a local ffmpeg fallback path from the packaged skill and replaced it with configurable ffmpeg lookup.
- Raised the fixed bilingual subtitle profile after comparing against Bilibili reference videos from 影视飓风 and MrBeast官方账号.
- Added the Local Translate subtitle and description path, with run-log and failed-segment checks when `translation_provider: local` is selected.
- Added `config/defaults.json` and switched the translation default back to the current agent model, while keeping Local Translate selectable through `translation_provider: local`.
- Made the default job values explicit: bilingual subtitles, thumbnail download enabled, and no cover editing unless requested.
