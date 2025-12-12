import tkinter as tk
from tkinter import ttk, messagebox


# =======================
#  FUNGSI MATEMATIKA RSA
# =======================

def egcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = egcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y


def modinv(e, phi):
    gcd, x, y = egcd(e, phi)
    if gcd != 1:
        return None  # Tidak punya invers
    return x % phi


# =======================
#  ENKRIPSI RSA
# =======================

def rsa_encrypt(plaintext, e, n):
    cipher_nums = [(ord(char) ** e) % n for char in plaintext]
    cipher_hex = " ".join([hex(c)[2:] for c in cipher_nums])
    return cipher_hex


# =======================
#  EVENT BUTTON
# =======================

def do_encrypt():
    try:
        plaintext = entry_plaintext.get()
        e = int(entry_e.get())
        n = int(entry_n.get())

        if plaintext.strip() == "":
            messagebox.showwarning("Warning", "Plainteks tidak boleh kosong!")
            return

        cipher = rsa_encrypt(plaintext, e, n)
        result_cipher.delete(0, tk.END)
        result_cipher.insert(0, cipher)

    except Exception as err:
        messagebox.showerror("Error", str(err))


# =======================
#  GUI UTAMA
# =======================

root = tk.Tk()
root.title("RSA Encryption (Latihan 1)")
root.geometry("550x300")
root.resizable(False, False)

frame = ttk.Frame(root, padding=20)
frame.pack(fill="both", expand=True)

# Label Judul
ttk.Label(frame, text="PROGRAM ENKRIPSI RSA", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

# Input Plainteks
ttk.Label(frame, text="Plainteks:").grid(row=1, column=0, sticky="w")
entry_plaintext = ttk.Entry(frame, width=40)
entry_plaintext.grid(row=1, column=1, pady=5)

# Key e
ttk.Label(frame, text="e (public key):").grid(row=2, column=0, sticky="w")
entry_e = ttk.Entry(frame, width=40)
entry_e.grid(row=2, column=1, pady=5)
entry_e.insert(0, "7")  # default

# Key n
p = 17
q = 11
n_default = p * q  # n = 187

ttk.Label(frame, text="n (p*q):").grid(row=3, column=0, sticky="w")
entry_n = ttk.Entry(frame, width=40)
entry_n.grid(row=3, column=1, pady=5)
entry_n.insert(0, str(n_default))

# Tombol Enkripsi
btn_encrypt = ttk.Button(frame, text="Enkripsi", command=do_encrypt)
btn_encrypt.grid(row=4, column=0, columnspan=2, pady=10)

# Output Cipher
ttk.Label(frame, text="Cipherteks (heksadesimal):").grid(row=5, column=0, sticky="w")
result_cipher = ttk.Entry(frame, width=40)
result_cipher.grid(row=5, column=1, pady=5)

root.mainloop()
