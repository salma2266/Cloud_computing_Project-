import subprocess
import shutil
import os

def create_virtual_disk():
    print("\n=== Create Virtual Disk ===")
    disk_name = input("Enter disk name (e.g., mydisk.qcow2): ").strip()
    disk_size = input("Enter disk size (e.g., 10G): ").strip()
    disk_format = input("Enter disk format (qcow2/raw): ").strip()

    # Check if qemu-img is installed
    if not shutil.which("qemu-img"):
        print("Error: qemu-img not installed!")
        return

    # Create command
    command = ["qemu-img", "create", "-f", disk_format, disk_name, disk_size]

    try:
        subprocess.run(command, check=True)
        print(f"Virtual disk '{disk_name}' created successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error creating virtual disk: {e}")

if __name__ == "__main__":
    create_virtual_disk()
