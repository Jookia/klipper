# Klipper TMC2209F branch #

## How to use ##

Ideally you should follow proper Klipper documentation, but for testing this tutorial should be sufficient to get up you and running.

(Run all these commands in the same directory as the README)

First, build the firmware. You will need arm-none-eabi-gcc build tools installed:

```
cp kobra.cfg .config
make
```

Copy 'out/klipper.bin' to 'firmware.bin' on an empty FAT32 SD card, put it in your Kobra and power it. It should beep I think? Turn it off after a minute or so.

If you really don't want to build firmware, grab the klipper.bin from https://github.com/SteveGotthardt/klipper/releases/tag/pre-merge .

Now connect your computer to the printer and run these commands:

```
python -m venv venv
source venv/bin/activate
pip install -r ./scripts/klippy-requirements.txt
python klippy/klippy.py ./kobra_xhack.cfg
```

Now in another window run:

```
echo G28 > /tmp/printer
```

This should center the printer and confirm the X axis is working.

**WARNING:** My settings may be broken on your printer. If this is the case this will make a really loud noise as the printer tries to slam the X rail itself in to the side. Be prepared to turn the printer off.

You can also just mess around with the printer and type command using this:

```
cat /dev/stdin >/tmp/printer | cat /tmp/printer
```

Tell me how it goes!

## Background ##

The Anycubic Kobra and any other boards that share the Trigorilla_Pro_A_V1.0.4
motherboard have a defect: The TMC2208 for the extruder and the TMC2209 for the
X axis share the same bus address. This bus is used for some error checking, and controller configuration.

One way to solve this is by moving a resistor on the board and configuring
Klipper as usual. See here: https://klipper.discourse.group/t/support-for-hdsc-chips-hc32f460/2860/54 . This method is risky if you aren't good with soldering and breaks support with original firmware. Not great.

Anycubic's Marlin firmware takes what I call the 'spray and pray' approach to this issue: Write to the chips as if they were addressed separately, don't do error checking, and hope things stay consistent.

This code takes a similar but different approach: Treat the two chips as one 'mega chip' with one set of registers that you write to and drive two stepper motors with. Error checking and status checking is disabled, but writes are done multiple times to compensate. I call this the TMC2209F controlled because it's kind of f*cked up.

In practice this code seems to work fine. This is probably because:

- Configuration only needs to be done at startup
- Other writes are only done during homing for the X axis
- The extruder ignores the end stop detection configuration anyway
- Reads are only really used for status updates and detecting lost transmissions, things that don't affect printing too much

I wrote and tested this code in like 5 hours, there's a lot of room for improvement.

# TODO #

- Add back support for setting registers using Klipper commands
- Simplify code to be a 'TMC2209 stepper + TMC2208 extruder' fix
- See what actually when reading registers- can we gain any information from it?
