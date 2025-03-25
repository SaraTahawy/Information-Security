import tkinter as tk
from tkinter import messagebox
import itertools
from string import ascii_letters

DICTIONARY_FILE = "Most.txt" 

def load_dictionary():
    try:
        with open(DICTIONARY_FILE, "r") as file:
            return [line.strip() for line in file]
    except FileNotFoundError:
        messagebox.showerror("Error", f"File not found: {DICTIONARY_FILE}")
        return []

def dictionary_attack():
    correct_password = entry_password.get()

    # To cheak the Password exactly 5 char
    if len(correct_password) != 5:
        messagebox.showwarning("Input Error", "Password must be exactly 5 characters long.")
        return

    dictionary = load_dictionary()
    if not dictionary:
        return

    if correct_password in dictionary:
        messagebox.showinfo("Success", "Welcome! Password found in dictionary.")
        return

    messagebox.showwarning("Failed", "Password not found in dictionary. Starting brute force attack...")
    brute_force_attack(correct_password)

def brute_force_attack(correct_password):
    
    for attempt in itertools.product(ascii_letters, repeat=5):  # try all possible triles
        attempt_password = "".join(attempt)
        if attempt_password == correct_password:
            messagebox.showinfo("Success", "Welcome! Password cracked by brute force.")
            return

    messagebox.showerror("Failed", "Brute force attack failed. Password not found.")

# GUI
root = tk.Tk()
root.title("Password Cracker")
root.geometry("300x200")

tk.Label(root, text="Enter Password (5 characters):").pack(pady=5)
entry_password = tk.Entry(root) 
entry_password.pack(pady=5)

tk.Button(root, text="Start Attack", command=dictionary_attack).pack(pady=10)

root.mainloop()




