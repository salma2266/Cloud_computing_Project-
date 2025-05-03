import tkinter as tk
from tkinter import messagebox
import subprocess
import shutil
import glob

# Function to list available virtual disks
def list_virtual_disks():
    return glob.glob("*.qcow2") + glob.glob("*.raw")

# Function to create virtual disk with GUI input
def create_virtual_disk():
    def on_submit():
        disk_name = name_entry.get().strip()
        disk_size = size_entry.get().strip()
        disk_format = format_entry.get().strip()

        if not disk_name or not disk_size or not disk_format:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        if not shutil.which("qemu-img"):
            messagebox.showerror("Error", "qemu-img not installed!")
            return

        command = ["qemu-img", "create", "-f", disk_format, disk_name, disk_size]
        try:
            subprocess.run(command, check=True)
            messagebox.showinfo("Success", f"Virtual disk '{disk_name}' created successfully!")
            top.destroy()
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Error creating virtual disk: {e}")

    top = tk.Toplevel(root)
    top.title("Create Virtual Disk")

    tk.Label(top, text="Disk Name (e.g., mydisk.qcow2):").pack()
    name_entry = tk.Entry(top)
    name_entry.pack()

    tk.Label(top, text="Disk Size (e.g., 10G):").pack()
    size_entry = tk.Entry(top)
    size_entry.pack()

    tk.Label(top, text="Disk Format (qcow2/raw):").pack()
    format_entry = tk.Entry(top)
    format_entry.pack()

    tk.Button(top, text="Create", command=on_submit).pack(pady=10)

# Function to create virtual machine with GUI input
def create_virtual_machine():
    def on_submit():
        cpu = cpu_entry.get().strip()
        memory = memory_entry.get().strip()
        iso_path = iso_entry.get().strip()

        if not cpu or not memory:
            messagebox.showerror("Error", "CPU and Memory are required.")
            return

        disks = list_virtual_disks()
        if not disks:
            messagebox.showerror("Error", "No virtual disks found. Please create a disk first.")
            return

        selected_disk = disk_var.get()
        if not selected_disk:
            messagebox.showerror("Error", "Please select a virtual disk.")
            return

        command = [
            "qemu-system-x86_64",
            "-display", "sdl",
            "-m", memory,
            "-smp", cpu,
            "-hda", selected_disk
        ]

        if iso_path:
            command += ["-cdrom", iso_path, "-boot", "d"]

        try:
            subprocess.run(command)
            messagebox.showinfo("Success", "Virtual Machine started successfully!")
            top.destroy()
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Error starting Virtual Machine: {e}")

    top = tk.Toplevel(root)
    top.title("Create Virtual Machine")

    tk.Label(top, text="Number of CPU cores (e.g., 2):").pack()
    cpu_entry = tk.Entry(top)
    cpu_entry.pack()

    tk.Label(top, text="Memory size in MB (e.g., 2048):").pack()
    memory_entry = tk.Entry(top)
    memory_entry.pack()

    tk.Label(top, text="Path to ISO file (optional):").pack()
    iso_entry = tk.Entry(top)
    iso_entry.pack()

    disks = list_virtual_disks()
    disk_var = tk.StringVar(top)
    if disks:
        disk_var.set(disks[0])  # Default selection
        tk.Label(top, text="Select a virtual disk:").pack()
        tk.OptionMenu(top, disk_var, *disks).pack()
    else:
        tk.Label(top, text="No virtual disks available!").pack()

    tk.Button(top, text="Start VM", command=on_submit).pack(pady=10)

# Setup main window
root = tk.Tk()
root.title("Virtual Machine & Disk Creator")
root.geometry("400x300")

tk.Button(root, text="Create Virtual Disk", width=30, command=create_virtual_disk).pack(pady=20)
tk.Button(root, text="Create Virtual Machine", width=30, command=create_virtual_machine).pack(pady=20)

root.mainloop()

