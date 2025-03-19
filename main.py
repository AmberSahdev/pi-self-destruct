"""
Self-destruct for Raspberry Pi

(This is a novelty project after watching too many Mission Impossibles)

The self-destruct sequence starts with disabling all comms (USB, ssh, eth, etc),
then moves on to burning the SD card and short-circuiting the board,
if it's somehow still alive it starts overclocking the CPU and overwriting data.

Materials Required:
- Raspberry Pi
- Jumper cables
- Nichrome wire
- Two MOSFET transistors or relay switches
- Optionally a cotton ball
"""
import os
import sys
import time

import RPi.GPIO as GPIO

SAFE_MODE = True  # Set to False to enable real destruction

# GPIO Pin Assignments
GPIO_SD_IGNITION = 27  # MOSFET for SD card ignition
GPIO_BOARD_SHORT = 22  # MOSFET for board short-circuit

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_SD_IGNITION, GPIO.OUT)
GPIO.setup(GPIO_BOARD_SHORT, GPIO.OUT)


def countdown_timer(seconds=100):
    print("\n**WARNING! SELF-DESTRUCTION INITIATED!**")
    print("\tCTRL+C to cancel\n")

    for i in range(seconds, 0, -1):
        bar = "#" * (i // 2) + "-" * ((seconds // 2) - (i // 2))
        sys.stdout.write(f"\rSeconds Remaining: [{bar}] {i}")
        sys.stdout.flush()
        time.sleep(1)

    print("\nGame Over\n")


# Kill Networking & USB
def disable_network_usb():
    print("Disabling Networking & USB...")
    if not SAFE_MODE:
        os.system("nohup sudo ip link set wlan0 down & disown")
        os.system("nohup sudo ip link set eth0 down & disown")
        os.system("nohup echo '1' | sudo tee /sys/devices/platform/soc/fe980000.usb/buspower & disown")
    else:
        print("SAFE MODE: Network & USB shutdown is disabled.")


# Overwrite SD Card
def overwrite_sd_card():
    print("Overwriting SD Card...")
    if not SAFE_MODE:
        os.system("nohup sudo dd if=/dev/urandom of=/dev/mmcblk0 bs=4M status=progress & disown")
    else:
        print("SAFE MODE: SD card wipe is disabled.")


# Overclock CPU for Thermal Damage
def overclock_cpu():
    print("Overclocking CPU...")
    if not SAFE_MODE:
        os.system("nohup bash -c 'echo force_turbo=1 >> /boot/config.txt && "
                  "echo over_voltage=6 >> /boot/config.txt && "
                  "echo arm_freq=2800 >> /boot/config.txt && "
                  "echo gpu_freq=900 >> /boot/config.txt && "
                  "echo temp_limit=0 >> /boot/config.txt && "
                  "stress --cpu 4 --timeout 600' & disown")
    else:
        print("SAFE MODE: CPU overclocking is disabled.")


# Ignite SD Card (Nichrome Wire + Cotton Ball)
def ignite_sd_card():
    print("Igniting SD Card with Nichrome Wire...")
    if not SAFE_MODE:
        GPIO.output(GPIO_SD_IGNITION, GPIO.HIGH)
        time.sleep(5)  # Keep heating for 5 seconds
        GPIO.output(GPIO_SD_IGNITION, GPIO.LOW)
    else:
        print("SAFE MODE: SD card ignition is disabled.")


# Short Circuit the Board (Kill Switch)
def short_circuit_board():
    print("Triggering Board Short Circuit...")
    if not SAFE_MODE:
        GPIO.output(GPIO_BOARD_SHORT, GPIO.HIGH)
        time.sleep(2)
        # GPIO.output(GPIO_BOARD_SHORT, GPIO.LOW)
    else:
        print("SAFE MODE: Board short-circuit is disabled.")


# Kernel Panic (in case it's not already dead)
def trigger_kernel_panic():
    print("Triggering Kernel Panic...")
    if not SAFE_MODE:
        os.system("echo c | sudo tee /proc/sysrq-trigger")
    else:
        print("SAFE MODE: Kernel panic is disabled.")


def main():
    countdown_timer()
    print("Raspberry Pi Self-Destruction Sequence Initiated")

    # Stage 1 
    disable_network_usb()  # Prevent override

    # Stage 2
    ignite_sd_card()  # Burn SD card
    short_circuit_board()  # Kill power

    # Stage 3 (if still operational)
    overwrite_sd_card()  # Start SD card overwrite
    overclock_cpu()  # Overheat CPU
    time.sleep(10)

    # Stage 4
    trigger_kernel_panic()  # Final OS crash (if still running)
    GPIO.cleanup()  # Reset GPIO pins


if __name__ == "__main__":
    main()
