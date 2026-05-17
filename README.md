# YouTube 中文字幕 Skill

中文 | [English](README.en.md)

把 YouTube 视频或本地视频做成可验收的中文字幕成片。

这个 skill 不是只“加一层字幕”。它会把字幕文件、烧录样式、封面预览、简介和审阅记录一起留下，方便以后复查、修改和复用。

## 安装

把 skill 目录复制或解包到你的 agent skills 目录。

Daniel 本机 Do Agent 使用：

```bash
mkdir -p /Users/daniel/.agents/skills
rsync -a youtube-cn-subtitle-burnin/ /Users/daniel/.agents/skills/youtube-cn-subtitle-burnin/
```

Codex 类环境请使用当前 Codex 配置的 skills 目录。

安装完成后，直接让 agent 使用 `youtube-cn-subtitle-burnin` 处理视频任务。

## 使用示例

```text
用 youtube-cn-subtitle-burnin，把这个 YouTube 视频做成中文字幕版。
需要保留 SRT 和 ASS，封面只加“中文字幕”和作者来源，不翻译原封面文字。
```

也可以这样要求双语：

```text
用 youtube-cn-subtitle-burnin 做中英双语硬字幕版。
中文作为主字幕，英文作为小号参考行，最终保留 MP4、SRT、ASS 和审阅截图。
```

## 你需要提供什么

- YouTube 链接，或本地视频文件
- 是否要中文-only，还是中英双语
- 是否需要处理封面
- 如果有固定术语、产品名或翻译偏好，也可以一起提供

## 它会交付什么

- 带硬字幕的 MP4
- 中文字幕 SRT
- 烧录样式 ASS
- 双语模式下的英文 SRT 和双语 ASS
- 原始封面、编辑后封面，以及 320px 缩略图预览
- 原始简介和中文简介
- 预览片、设计确认图、最终截图和审阅记录

## 适合谁用

- 想把英文 YouTube 技术视频转成中文学习版
- 想给课程、访谈、工具演示视频加中文字幕或中英双语字幕
- 想要一套稳定流程，而不是每次临时调字幕样式
- 想保留 SRT / ASS，不希望只拿到一个烧录后的 MP4

## 它重点解决什么

- 字幕样式不稳定：固定中文-only 和双语字幕样式
- 双语不对应：抽查中文、英文和语音时间是否对得上
- 自动字幕质量差：先清理断句、重叠、空白和悬空句尾
- 封面处理不统一：明确保留原文、翻译原文、中文化改写三种模式
- 交付不可复用：默认保留 SRT、ASS、截图和审阅记录

## 质量门槛

每个正式视频都要先过这些检查：

- 预览片里必须能看到字幕
- 字幕必须在手机尺寸下可读
- 字幕样式必须匹配固定模板
- 双语字幕必须有对应关系抽查
- 封面必须看 320px 缩略图效果
- 最终 MP4 必须检查音画、截图和文件完整性

## 依赖

- Python
- ffmpeg / ffprobe
- yt-dlp
- Pillow
- 一个能执行该 skill 的 agent 模型，用于翻译、判断和审阅

## 维护者说明

修改 `youtube-cn-subtitle-burnin/` 下的文件后，刷新打包文件：

```bash
rm -f dist/youtube-cn-subtitle-burnin.skill
mkdir -p dist
zip -r dist/youtube-cn-subtitle-burnin.skill youtube-cn-subtitle-burnin
```

发布或安装前运行：

```bash
python3 -m py_compile youtube-cn-subtitle-burnin/scripts/*.py
for f in youtube-cn-subtitle-burnin/scripts/*.py; do python3 "$f" --help >/dev/null || exit 1; done
unzip -l dist/youtube-cn-subtitle-burnin.skill
```

## 流程概览

<img src="assets/youtube-cn-subtitle-skill-infographic.png" alt="YouTube 中文字幕 Skill 信息图" width="560">

## 开源说明

本项目使用 MIT License。
