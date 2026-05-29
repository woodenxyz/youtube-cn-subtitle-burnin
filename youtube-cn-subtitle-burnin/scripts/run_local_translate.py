#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


DEFAULT_LOCAL_TRANSLATE = Path.home() / ".agents/skills/local-translate/scripts/local_translate.py"
SRT_TIME = re.compile(r"^\d{2}:\d{2}:\d{2},\d{3}\s+-->\s+\d{2}:\d{2}:\d{2},\d{3}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run Local Translate and copy a verified result to the video job output path."
    )
    parser.add_argument("input", type=Path, help="Input SRT, Markdown, or text file")
    parser.add_argument("--out", type=Path, required=True, help="Final output path to write")
    parser.add_argument(
        "--runs-dir",
        type=Path,
        help="Directory where Local Translate should save timestamped run folders",
    )
    parser.add_argument(
        "--format",
        choices=["auto", "text", "markdown", "srt"],
        default="auto",
        help="Input format passed to Local Translate",
    )
    parser.add_argument("--target-language", default="Simplified Chinese")
    parser.add_argument("--model", help="Override the Local Translate model")
    parser.add_argument("--ollama-url", help="Override the Ollama URL")
    parser.add_argument("--max-chars", type=int, help="Maximum characters per translation segment")
    parser.add_argument("--timeout", type=int, help="Request timeout in seconds")
    parser.add_argument("--retries", type=int, help="Retry count per segment")
    parser.add_argument(
        "--local-translate-script",
        type=Path,
        default=DEFAULT_LOCAL_TRANSLATE,
        help="Path to local_translate.py",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite --out if it already exists")
    return parser.parse_args()


def srt_signature(path: Path) -> list[tuple[str, str]]:
    data = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    blocks = [block for block in re.split(r"\n{2,}", data.strip()) if block.strip()]
    signature: list[tuple[str, str]] = []
    for block in blocks:
        lines = [line.strip() for line in block.splitlines()]
        if len(lines) < 2 or not lines[0].isdigit() or not SRT_TIME.match(lines[1]):
            raise ValueError(f"invalid SRT block in {path}: {lines[:2]}")
        signature.append((lines[0], lines[1]))
    if not signature:
        raise ValueError(f"no SRT cues found in {path}")
    return signature


def parse_summary(stdout: str) -> dict[str, Any]:
    lines = [line.strip() for line in stdout.splitlines() if line.strip()]
    if not lines:
        raise ValueError("Local Translate printed no JSON summary")
    return json.loads(lines[-1])


def add_option(command: list[str], flag: str, value: object | None) -> None:
    if value is not None:
        command.extend([flag, str(value)])


def main() -> int:
    args = parse_args()
    input_path = args.input.expanduser().resolve()
    out_path = args.out.expanduser().resolve()
    script_path = args.local_translate_script.expanduser().resolve()
    runs_dir = (
        args.runs_dir.expanduser().resolve()
        if args.runs_dir
        else input_path.parent / "local-translate-runs"
    )

    if not input_path.is_file():
        print(f"FAIL: missing input file {input_path}")
        return 1
    if not script_path.is_file():
        print(f"FAIL: missing Local Translate script {script_path}")
        return 1
    if out_path.exists() and not args.force:
        print(f"FAIL: output already exists, choose a new version or pass --force: {out_path}")
        return 1

    command = [
        sys.executable,
        str(script_path),
        str(input_path),
        "--output-dir",
        str(runs_dir),
        "--format",
        args.format,
        "--target-language",
        args.target_language,
        "--json",
    ]
    add_option(command, "--model", args.model)
    add_option(command, "--ollama-url", args.ollama_url)
    add_option(command, "--max-chars", args.max_chars)
    add_option(command, "--timeout", args.timeout)
    add_option(command, "--retries", args.retries)

    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    try:
        summary = parse_summary(completed.stdout)
    except (ValueError, json.JSONDecodeError) as exc:
        print(f"FAIL: could not parse Local Translate summary: {exc}")
        if completed.stdout.strip():
            print(completed.stdout.strip())
        if completed.stderr.strip():
            print(completed.stderr.strip())
        return completed.returncode or 1

    failed_count = int(summary.get("failed_segment_count", -1))
    failures_file = Path(str(summary.get("failed_segments_file", ""))).expanduser()
    run_log = Path(str(summary.get("run_log_file", ""))).expanduser()
    translated_file = Path(str(summary.get("output_file", ""))).expanduser()

    if completed.returncode != 0 or failed_count != 0:
        print(f"FAIL: Local Translate reported {failed_count} failed segment(s)")
        print(f"Failed segments: {failures_file}")
        print(f"Run log: {run_log}")
        return completed.returncode or 1
    if not translated_file.is_file():
        print(f"FAIL: translated output missing: {translated_file}")
        return 1

    effective_format = args.format
    if effective_format == "auto" and input_path.suffix.lower() == ".srt":
        effective_format = "srt"
    if effective_format == "srt" and srt_signature(input_path) != srt_signature(translated_file):
        print("FAIL: translated SRT changed cue numbers or timestamps")
        print(f"Source: {input_path}")
        print(f"Translated: {translated_file}")
        return 1

    out_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(translated_file, out_path)
    print(f"PASS: wrote {out_path}")
    print(f"PASS: Local Translate run log: {run_log}")
    print(f"PASS: Local Translate failed segments: {failures_file} ({failed_count})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
