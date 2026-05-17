# YouTube 中文字幕 Skill

中文 | [English](README.en.md)

这个仓库维护 `youtube-cn-subtitle-burnin` Agent Skill。

它把 YouTube 链接、本地视频或已有字幕文件处理成可验收的中文字幕成片。默认交付不只是一条 MP4，还会保留可复用字幕文件、封面预览、简介和审阅记录。

![YouTube 中文字幕 Skill 信息图](assets/youtube-cn-subtitle-skill-infographic.png)

## 包含内容

- `assets/youtube-cn-subtitle-skill-infographic.png` - skill 能力概览图
- `youtube-cn-subtitle-burnin/SKILL.md` - skill 主说明
- `youtube-cn-subtitle-burnin/references/` - 运行流程、质量门槛、审阅模板和反馈记录
- `youtube-cn-subtitle-burnin/scripts/` - 字幕清理、翻译批次、固定样式 ASS、双语对齐检查、封面预览、预览片、烧录、截图和验收工具
- `dist/youtube-cn-subtitle-burnin.skill` - 打包后的 skill 文件

## 安装

把 skill 目录复制或解包到你的 agent skills 目录。

Daniel 本机 Do Agent 使用：

```bash
mkdir -p /Users/daniel/.agents/skills
rsync -a youtube-cn-subtitle-burnin/ /Users/daniel/.agents/skills/youtube-cn-subtitle-burnin/
```

Codex 类环境请使用当前 Codex 配置的 skills 目录。

## 打包

修改 `youtube-cn-subtitle-burnin/` 下的文件后，刷新打包文件：

```bash
rm -f dist/youtube-cn-subtitle-burnin.skill
mkdir -p dist
zip -r dist/youtube-cn-subtitle-burnin.skill youtube-cn-subtitle-burnin
```

## 验证

发布或安装前运行：

```bash
python3 -m py_compile youtube-cn-subtitle-burnin/scripts/*.py
for f in youtube-cn-subtitle-burnin/scripts/*.py; do python3 "$f" --help >/dev/null || exit 1; done
unzip -l dist/youtube-cn-subtitle-burnin.skill
```

## 工作约定

真实视频任务里，这个 skill 要求 agent 做到：

1. 保留原始视频信息、封面和简介
2. 生成可复用的中文字幕 SRT 和烧录样式 ASS；双语模式下同时保留英文 SRT 和双语 ASS
3. 先检查源视频是否已有内嵌字幕，再决定是否使用双语布局
4. 默认使用固定字幕样式；只有遮挡关键画面时才使用上移样式
5. 双语模式必须抽查中英文和语音时间是否对应
6. 封面处理必须记录模式，并检查 320px 缩略图预览
7. 全量烧录前先生成带字幕预览片
8. 全量烧录前抽取设计确认图
9. 检查最终 MP4 的音画
10. 抽取最终审阅截图
11. 写入审阅记录
12. 把可复用问题回写到 skill 的参考文件里

旧的 MP4、SRT 和 ASS 不应被覆盖。重新生成时使用新的版本号文件名。

## 开源说明

本项目使用 MIT License。
