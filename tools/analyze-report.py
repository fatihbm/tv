#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import re
import sys


def read(path: pathlib.Path) -> str:
    try:
        return path.read_text(errors="replace")
    except FileNotFoundError:
        return ""


def first(pattern: str, text: str, flags: int = re.I | re.M) -> str | None:
    match = re.search(pattern, text, flags)
    return match.group(1).strip() if match else None


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} artifacts/<timestamp>", file=sys.stderr)
        return 1

    root = pathlib.Path(sys.argv[1])
    cpu = read(root / "cpuinfo.txt")
    uname = read(root / "uname.txt")
    cmdline = read(root / "cmdline.txt")
    partitions = read(root / "partitions.txt")
    mounts = read(root / "mounts.txt")
    dmesg = read(root / "dmesg.txt")

    arch = first(r"^(?:Architecture|model name|Processor)\s*:\s*(.+)$", cpu)
    machine = first(r"^(?:Hardware|machine)\s*:\s*(.+)$", cpu)

    hints: list[str] = []
    haystack = "\n".join([cpu, uname, cmdline, dmesg]).lower()

    for token in ["mstar", "mediatek", "realtek", "broadcom", "arm", "mips"]:
        if token in haystack:
            hints.append(token)

    block_lines = [
        line.strip()
        for line in partitions.splitlines()
        if re.search(r"\b(mmcblk|mtd|ubi|nand|sda)\w*\b", line)
    ]

    print("# TV Portability Report")
    print()
    print(f"- Kernel: {uname.strip() or 'unknown'}")
    print(f"- CPU: {arch or 'unknown'}")
    print(f"- Machine/board hint: {machine or 'unknown'}")
    print(f"- SoC/architecture hints: {', '.join(sorted(set(hints))) or 'none detected'}")
    print(f"- Candidate storage entries: {len(block_lines)}")
    print()

    if block_lines:
        print("## Candidate storage layout")
        print("```text")
        for line in block_lines[:100]:
            print(line)
        print("```")
        print()

    print("## Portability gates")
    print("- [ ] Exact SoC and board revision identified")
    print("- [ ] Bootloader family/version identified")
    print("- [ ] Verified recovery/UART path")
    print("- [ ] Complete partition backup created and restored on spare media/board")
    print("- [ ] Kernel source/BSP or usable downstream kernel located")
    print("- [ ] Display/GPU/VPU drivers available")
    print("- [ ] Input/audio/network hardware mapped")
    print("- [ ] Alternate, non-destructive boot path demonstrated")
    print()

    if " / " in mounts:
        print("Root filesystem detected. Do not remount it read-write during discovery.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
