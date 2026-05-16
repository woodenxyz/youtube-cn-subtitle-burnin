#!/usr/bin/env python3
import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


SRT_TS = re.compile(r"(\d{2}:\d{2}:\d{2},\d{3})\s+-->\s+(\d{2}:\d{2}:\d{2},\d{3})")
ASS_TS = re.compile(r"Dialogue:[^,]*,([^,]+),([^,]+),[^,]*,[^,]*,[^,]*,[^,]*,[^,]*,[^,]*,(.*)")
HTML_TAG = re.compile(r"<[^>]+>")
ASS_OVERRIDE = re.compile(r"\{[^}]*\}")
HANGING_ENDINGS = (
    "所以，",
    "所以,",
    "并且",
    "而且",
    "然后",
    "然后会",
    "接下来",
    "接下来要",
    "我要",
    "它会",
    "这会",
    "因为",
    "如果",
    "当",
    "而",
    "但",
    "但是",
    "以及",
)
INCOMPLETE_PUNCTUATION = ("，", "、", "：", "；", ",", ":", ";")
PROTECTED_PHRASES = (
    "OpenAI Codex",
    "Claude Code",
    "ChatGPT",
    "GitHub",
    "Computer Use",
    "Browser Use",
    "MCP server",
    "Codex",
    "OpenAI",
    "Claude",
    "Chronicle",
)


@dataclass
class Cue:
    idx: int
    start: float
    end: float
    text: str


def parse_srt_time(value: str) -> float:
    hh, mm, rest = value.split(":")
    ss, ms = rest.split(",")
    return int(hh) * 3600 + int(mm) * 60 + int(ss) + int(ms) / 1000


def parse_ass_time(value: str) -> float:
    hh, mm, rest = value.strip().split(":")
    ss, cs = rest.split(".")
    return int(hh) * 3600 + int(mm) * 60 + int(ss) + int(cs) / 100


def normalize_text(text: str) -> str:
    text = text.replace("\\N", "\n").replace("\\n", "\n")
    text = ASS_OVERRIDE.sub("", text)
    text = HTML_TAG.sub("", text)
    text = re.sub(r"\s+", "", text)
    return text.strip()


def visible_text(text: str) -> str:
    text = text.replace("\\N", "\n").replace("\\n", "\n")
    text = ASS_OVERRIDE.sub("", text)
    text = HTML_TAG.sub("", text)
    return text.strip()


def check_line_breaks(text: str) -> list[str]:
    issues: list[str] = []
    visible = visible_text(text)
    if "\n" not in visible:
        return issues
    with_line_breaks = re.sub(r"[ \t\r\f\v]+", "", visible)
    raw = re.sub(r"\s+", "", visible)
    for phrase in PROTECTED_PHRASES:
        phrase_key = re.sub(r"\s+", "", phrase)
        if phrase_key in raw and phrase_key not in with_line_breaks:
            issues.append(f"protected phrase split across line break: {phrase}")
    lines = [line.strip() for line in visible.splitlines() if line.strip()]
    for left, right in zip(lines, lines[1:]):
        if re.search(r"[A-Za-z0-9]$", left) and re.search(r"^[A-Za-z0-9]", right):
            issues.append(f"English/number token split across line break: {left[-12:]} / {right[:12]}")
    return issues


def parse_srt(path: Path) -> list[Cue]:
    blocks = re.split(r"\n\s*\n", path.read_text(encoding="utf-8-sig").strip())
    cues: list[Cue] = []
    for block in blocks:
        lines = [line.rstrip() for line in block.splitlines() if line.strip()]
        if not lines:
            continue
        ts_line_index = next((i for i, line in enumerate(lines) if SRT_TS.search(line)), None)
        if ts_line_index is None:
            continue
        match = SRT_TS.search(lines[ts_line_index])
        assert match is not None
        raw_idx = lines[0] if ts_line_index > 0 else str(len(cues) + 1)
        idx = int(raw_idx) if raw_idx.isdigit() else len(cues) + 1
        text = "\n".join(lines[ts_line_index + 1 :])
        cues.append(Cue(idx, parse_srt_time(match.group(1)), parse_srt_time(match.group(2)), text))
    return cues


def parse_ass(path: Path) -> list[Cue]:
    cues: list[Cue] = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        match = ASS_TS.match(line)
        if not match:
            continue
        cues.append(Cue(len(cues) + 1, parse_ass_time(match.group(1)), parse_ass_time(match.group(2)), match.group(3)))
    return cues


def parse_subtitle(path: Path) -> list[Cue]:
    suffix = path.suffix.lower()
    if suffix == ".srt":
        return parse_srt(path)
    if suffix == ".ass":
        return parse_ass(path)
    raise SystemExit(f"Unsupported subtitle format: {path.suffix}")


def check(cues: list[Cue], min_duration: float, overlap_tolerance: float, strict_short: bool) -> tuple[list[str], list[str]]:
    issues: list[str] = []
    warnings: list[str] = []
    ordered = sorted(cues, key=lambda cue: (cue.start, cue.end, cue.idx))
    for cue in ordered:
        text = normalize_text(cue.text)
        duration = cue.end - cue.start
        if not text:
            issues.append(f"empty cue #{cue.idx} at {cue.start:.3f}s")
        if duration <= 0:
            issues.append(f"non-positive duration cue #{cue.idx}: {duration:.3f}s")
        elif duration < min_duration:
            message = f"short cue #{cue.idx}: {duration:.3f}s"
            if strict_short:
                issues.append(message)
            else:
                warnings.append(message)
        if duration > 9.0 and len(text) > 70:
            warnings.append(f"dense cue #{cue.idx}: {duration:.3f}s, {len(text)} normalized chars")
        if len(text) > 110:
            warnings.append(f"long text cue #{cue.idx}: {len(text)} normalized chars")
        if any(text.endswith(ending) for ending in HANGING_ENDINGS):
            issues.append(f"dangling ending cue #{cue.idx}: {text[-30:]}")
        elif text.endswith(INCOMPLETE_PUNCTUATION):
            issues.append(f"incomplete punctuation cue #{cue.idx}: {text[-30:]}")
        for line_break_issue in check_line_breaks(cue.text):
            issues.append(f"bad line break cue #{cue.idx}: {line_break_issue}")
    for previous, current in zip(ordered, ordered[1:]):
        if current.start < previous.end - overlap_tolerance:
            issues.append(
                f"overlap cue #{previous.idx} -> #{current.idx}: "
                f"{previous.end - current.start:.3f}s"
            )
    return issues, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Check SRT/ASS subtitle timing and semantic-screen risks.")
    parser.add_argument("subtitle", type=Path)
    parser.add_argument("--min-duration", type=float, default=0.8)
    parser.add_argument("--overlap-tolerance", type=float, default=0.02)
    parser.add_argument("--strict-short", action="store_true", help="Fail on cues shorter than --min-duration")
    args = parser.parse_args()

    cues = parse_subtitle(args.subtitle)
    if not cues:
        print(f"FAIL {args.subtitle}: no cues found")
        return 1

    issues, warnings = check(cues, args.min_duration, args.overlap_tolerance, args.strict_short)
    print(f"Checked {len(cues)} cues in {args.subtitle}")
    if warnings:
        print(f"WARN: {len(warnings)} short cue warning(s)")
        for warning in warnings[:50]:
            print(f"- {warning}")
        if len(warnings) > 50:
            print(f"- ... {len(warnings) - 50} more")
    if issues:
        print(f"FAIL: {len(issues)} issue(s)")
        for issue in issues[:200]:
            print(f"- {issue}")
        if len(issues) > 200:
            print(f"- ... {len(issues) - 200} more")
        return 1
    print("PASS: no overlap, empty cues, or dangling endings found")
    return 0


if __name__ == "__main__":
    sys.exit(main())
