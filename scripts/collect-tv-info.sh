#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-}"
if [[ -z "$TARGET" ]]; then
  echo "Usage: $0 user@tv-ip" >&2
  exit 1
fi

STAMP="$(date +%Y%m%d-%H%M%S)"
OUT="artifacts/$STAMP"
mkdir -p "$OUT"

run() {
  local name="$1"
  shift
  echo "[collect] $name"
  ssh -o ConnectTimeout=5 "$TARGET" "$@" >"$OUT/$name.txt" 2>&1 || true
}

# Read-only discovery only. No dd, flashcp, nandwrite, mount -o rw or partition writes.
run uname 'uname -a'
run cpuinfo 'cat /proc/cpuinfo'
run meminfo 'cat /proc/meminfo'
run cmdline 'cat /proc/cmdline'
run mounts 'cat /proc/mounts'
run partitions 'cat /proc/partitions'
run filesystems 'cat /proc/filesystems'
run modules 'cat /proc/modules'
run devices 'cat /proc/devices'
run interrupts 'cat /proc/interrupts'
run version 'cat /proc/version'
run release 'cat /etc/*release 2>/dev/null || true'
run block 'ls -l /dev/block /dev/mmc* /dev/mtd* /dev/ubi* 2>/dev/null || true'
run sysblock 'for d in /sys/class/block/*; do echo "=== $d ==="; cat "$d/size" 2>/dev/null; cat "$d/ro" 2>/dev/null; done'
run devicetree 'find /proc/device-tree -maxdepth 3 -type f -print 2>/dev/null | sort | head -2000'
run bootdirs 'ls -la /boot /mnt /media /var 2>/dev/null || true'
run dmesg 'dmesg 2>/dev/null | tail -3000'
run network 'ip addr 2>/dev/null || ifconfig -a 2>/dev/null || true'
run processes 'ps -ef 2>/dev/null || ps aux 2>/dev/null || true'

cat >"$OUT/README.txt" <<EOF
Collected from: $TARGET
Timestamp: $STAMP
Mode: read-only discovery

Do not publish this directory before reviewing it for serial numbers, MAC addresses,
IP addresses, credentials or other device-specific identifiers.
EOF

echo "Report written to $OUT"
