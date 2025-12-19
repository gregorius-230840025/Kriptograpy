# =============================================================
# ALGORITMA ELGAMAL UNTUK PLAINTEXT TEKS (ASCII)
# Dengan Penjelasan Langkah & Tampilan (Tkinter GUI)
# =============================================================
# Plaintext dapat berupa teks (contoh: GREGORIUSSIH)
# =============================================================

import random
import tkinter as tk
from tkinter import ttk, messagebox

# -------------------------------------------------------------
# FUNGSI MATEMATIKA DASAR
# -------------------------------------------------------------

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def mod_exp(base, exp, mod):
    return pow(base, exp, mod)

# -------------------------------------------------------------
# PEMBANGKITAN KUNCI ELGAMAL
# -------------------------------------------------------------

def generate_keys(p, g):
    x = random.randint(1, p - 2)   # kunci privat
    y = mod_exp(g, x, p)           # kunci publik
    return x, y

# -------------------------------------------------------------
# ENKRIPSI & DEKRIPSI KARAKTER
# -------------------------------------------------------------

def encrypt_char(m, p, g, y):
    k = random.randint(1, p - 2)
    a = mod_exp(g, k, p)
    b = (m * mod_exp(y, k, p)) % p
    return a, b, k


def decrypt_char(a, b, p, x):
    s = mod_exp(a, x, p)
    s_inv = pow(s, -1, p)
    m = (b * s_inv) % p
    return m

# -------------------------------------------------------------
# GUI TKINTER
# -------------------------------------------------------------

root = tk.Tk()
root.title("Algoritma ElGamal (Plaintext Teks)")
root.geometry("800x650")

frame = ttk.Frame(root, padding=10)
frame.pack(fill="both", expand=True)

# INPUT

ttk.Label(frame, text="Bilangan Prima (p)").grid(row=0, column=0, sticky="w")
p_entry = ttk.Entry(frame)
p_entry.grid(row=0, column=1)


ttk.Label(frame, text="Generator (g)").grid(row=1, column=0, sticky="w")
g_entry = ttk.Entry(frame)
g_entry.grid(row=1, column=1)


ttk.Label(frame, text="Plaintext (Nama)").grid(row=2, column=0, sticky="w")
m_entry = ttk.Entry(frame, width=40)
m_entry.grid(row=2, column=1)

# OUTPUT

output = tk.Text(frame, height=22, width=90)
output.grid(row=6, column=0, columnspan=3, pady=10)

# -------------------------------------------------------------
# PROSES UTAMA
# -------------------------------------------------------------

def process():
    try:
        p = int(p_entry.get())
        g = int(g_entry.get())
        plaintext = m_entry.get()

        if not is_prime(p):
            messagebox.showerror("Error", "p harus bilangan prima")
            return
        if g <= 1 or g >= p:
            messagebox.showerror("Error", "g harus memenuhi 1 < g < p")
            return

        # Generate key
        x, y = generate_keys(p, g)

        output.delete("1.0", tk.END)
        output.insert(tk.END, "=== PEMBANGKITAN KUNCI ELGAMAL ===\n")
        output.insert(tk.END, f"Kunci Privat (x) = {x}\n")
        output.insert(tk.END, f"Kunci Publik (y) = {y}\n\n")

        ciphertext = []
        decrypted_text = ""

        output.insert(tk.END, "=== PROSES ENKRIPSI PER KARAKTER (ASCII) ===\n")

        for ch in plaintext:
            m = ord(ch)  # ASCII
            if m >= p:
                messagebox.showerror("Error", "Nilai ASCII karakter harus < p")
                return

            a, b, k = encrypt_char(m, p, g, y)
            ciphertext.append((a, b))

            output.insert(tk.END, f"Karakter '{ch}' -> ASCII {m}\n")
            output.insert(tk.END, f"  k = {k}\n")
            output.insert(tk.END, f"  a = {a}, b = {b}\n")

        output.insert(tk.END, "\n=== PROSES DEKRIPSI ===\n")

        for (a, b) in ciphertext:
            m_dec = decrypt_char(a, b, p, x)
            decrypted_text += chr(m_dec)

        output.insert(tk.END, f"Hasil Dekripsi: {decrypted_text}\n")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# BUTTON

ttk.Button(frame, text="Proses ElGamal", command=process).grid(row=5, column=0, columnspan=2, pady=10)

root.mainloop()

# =============================================================
# CATATAN AKADEMIS:
# - Setiap karakter dikonversi ke ASCII
# - Setiap ASCII dienkripsi menggunakan ElGamal
# - Ciphertext berupa pasangan (a, b)
# =============================================================
