# Feasibility: LG webOS 3 → Android TV / Google TV

## Confirmed target facts

For LG 43UH650V, LG documents webOS 3.0, 4K UHD, 3 HDMI inputs, 2 USB 2.0 ports, LAN, Simplink and an RS-232C control/service interface.

## What root access gives us

A rooted webOS environment can provide valuable board reconnaissance: kernel details, loaded drivers, partition layout, device tree information, logs and firmware metadata. It may also allow safe read-only extraction of data once the storage map is understood.

Root access **does not prove** that the bootloader is unlocked or that unsigned kernels can be booted.

## Why a direct Google TV image is not currently a realistic first step

Google TV runs on Android TV and depends on a board-specific Android software stack. A generic x86/ARM Android TV image cannot simply replace LG webOS firmware.

The critical dependencies are:

1. **Boot chain** — identify boot ROM, first/second-stage bootloader, signature verification and recovery behavior.
2. **Kernel/BSP** — an Android-capable kernel for the exact SoC/board.
3. **Display/GPU/VPU** — framebuffer/KMS, GPU acceleration and hardware video decode.
4. **Android HALs** — audio, input, network, HDMI, CEC and other hardware integration.
5. **Secure media** — Widevine/secure video path and keys are device/manufacturer specific.
6. **Google certification** — Google TV/GMS distribution is licensed and cannot be treated as a freely redistributable ROM.

## Decision tree

### A. Bootloader cannot load unsigned code

Stop the native Android-port path unless a reversible alternate boot method is found. Do not overwrite internal flash.

### B. Bootloader can load a custom kernel, but no usable BSP exists

A port may still be possible, but driver reverse engineering becomes the dominant project cost. The first milestone is a Linux console over UART, not Android UI.

### C. Bootloader + kernel/BSP are usable

Proceed with an AOSP/Android TV device port. Google services remain a separate certification/licensing concern.

## First physical-TV milestones

1. Confirm full model suffix and installed firmware.
2. Determine whether the installed firmware has a safe supported path to root/developer shell.
3. Run the read-only inventory collector.
4. Identify SoC and bootloader from the report.
5. Locate board documentation, GPL kernel source, firmware packages and recovery information.
6. Establish UART/service recovery before any write experiment.

## No-go criteria

Native conversion should be abandoned if all of the following are true:

- bootloader is cryptographically locked with no reversible alternate boot path;
- no usable source/BSP exists for the board;
- display/video drivers are proprietary and cannot be reused with Android;
- there is no reliable hardware recovery method.

In that case, the engineering-optimal solution is an HDMI Google TV device with CEC, leaving the LG board as display/tuner controller.
