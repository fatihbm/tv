# LG webOS → Android/Google TV Port Research

Target: LG 43UH650V-class televisions running webOS 3.0.

## Goal

Determine whether the original LG mainboard can boot an Android TV/AOSP-based system without replacing the board.

This repository intentionally starts with **non-destructive discovery and backup**. Do not flash partitions until the boot chain, recovery path, partition map, SoC, storage layout and signing requirements are understood.

## Important reality check

A webOS root shell is not equivalent to an unlocked bootloader. Running Google TV on the original board would require, at minimum:

- bootloader control or an alternate boot path;
- Linux/Android kernel support for the exact LG SoC and board;
- GPU/VPU/display/audio/input/network drivers;
- Android HALs and device tree / board configuration;
- working recovery and a complete flash backup;
- DRM/secure-video support for commercial streaming services.

Google TV and Google Mobile Services are proprietary/licensed components. Even if Android/AOSP can be booted, redistributing Google TV images is a separate licensing issue. The practical open-source target is therefore **AOSP/Android TV-compatible userspace**, with Google services treated as an optional, separately licensed layer.

## Project phases

### Phase 0 — Identify exact TV and firmware

Record the full model suffix (for example `43UH650V-ZB`) and firmware version from TV settings / rear label.

### Phase 1 — Obtain shell access safely

Prefer a supported developer/root method appropriate to the installed webOS firmware. Do not downgrade or modify firmware before creating a recovery plan.

### Phase 2 — Collect hardware and boot-chain inventory

From a Mac/Linux workstation:

```bash
./scripts/collect-tv-info.sh root@TV_IP
```

The script is read-only. It collects kernel, CPU, mounts, partitions, device tree, loaded modules and selected logs into `artifacts/`.

### Phase 3 — Assess portability

```bash
python3 tools/analyze-report.py artifacts/<timestamp>
```

This generates a summary of the SoC/architecture, storage layout and likely blockers.

### Phase 4 — Backup

Only after the storage map is verified, implement a board-specific backup procedure. Raw partition reads are deliberately not automated in the initial version.

### Phase 5 — Alternate boot PoC

Before touching internal flash, investigate UART/service access and whether the bootloader can load a kernel/initramfs from USB, network or a temporary RAM location.

### Phase 6 — AOSP bring-up

Only if Phase 5 succeeds:

1. Minimal kernel + initramfs console
2. Framebuffer/display
3. USB/network
4. Android userspace
5. Remote/input
6. Audio
7. Hardware video decode
8. DRM/streaming compatibility

## Safety rules

- Never write to `mmcblk*`, `mtd*`, `ubi*` or bootloader partitions during discovery.
- Never erase or format internal storage.
- Keep a copy of every original partition before the first write operation.
- Establish UART/recovery access before testing a custom boot image.
- Treat firmware files and proprietary LG binaries as copyrighted material; do not commit them to this repository.

## Current target

Expected model: **LG 43UH650V**, webOS 3.0. Exact suffix and firmware still need to be confirmed on the physical TV.
