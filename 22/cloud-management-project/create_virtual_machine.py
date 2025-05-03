import subprocess
import os
import glob

def list_virtual_disks():
    print("\nAvailable Virtual Disks:")
    disks = glob.glob("*.qcow2") + glob.glob("*.raw")
    for idx, disk in enumerate(disks):
        print(f"{idx + 1}. {disk}")
    return disks

def create_virtual_machine():
    print("\n=== Create Virtual Machine ===")
    cpu = input("Enter number of CPU cores (e.g., 2): ").strip()
    memory = input("Enter RAM size in MB (e.g., 2048): ").strip()

    # List available disks
    disks = list_virtual_disks()
    if not disks:
        print("No virtual disks found. Please create a disk first!")
        return

    disk_choice = int(input("Select a disk by number: ")) - 1
    selected_disk = disks[disk_choice]

    iso_path = input("Enter path to ISO file for installation (leave empty if none): ").strip()

    # Build command
    command = [
        "qemu-system-x86_64",
       "-display", "sdl",  
        "-m", memory,
        "-smp", cpu,
        "-hda", selected_disk,
        
    ]

    if iso_path:
        command += ["-cdrom", iso_path, "-boot", "d"]  # Boot from ISO if provided

    try:
        subprocess.run(command)
        print("Virtual Machine started successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error starting Virtual Machine: {e}")

if __name__ == "__main__":
    create_virtual_machine()
