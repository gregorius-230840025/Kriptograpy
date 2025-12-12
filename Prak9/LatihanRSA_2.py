import random
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog

# --------------------------------------------------------------------
#  UTIL PRIMA
# --------------------------------------------------------------------
def is_prime(n):
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    r = int(n**0.5)
    for i in range(3, r + 1, 2):
        if n % i == 0:
            return False

    return True

def random_prime_in_range(low, high):
    primes = [x for x in range(low, high + 1) if is_prime(x)]
    return random.choice(primes)

# --------------------------------------------------------------------
#  GCD, EGCD, MODINV
# --------------------------------------------------------------------
def egcd(a, b):
    if a == 0:
        return b, 0, 1
    g, y, x = egcd(b % a, a)
    return g, x - (b // a) * y, y

def modinv(e, phi):
    g, x, y = egcd(e, phi)
    if g != 1:
        return None
    return x % phi

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# --------------------------------------------------------------------
#  RSA GEN, ENCRYPT, DECRYPT
# --------------------------------------------------------------------
def generate_keypair_random(low, high, debug):
    p = random_prime_in_range(low, high)
    q = random_prime_in_range(low, high)
    while q == p:
        q = random_prime_in_range(low, high)

    debug.append(f"p = {p}")
    debug.append(f"q = {q}")

    n = p * q
    phi = (p - 1) * (q - 1)
    debug.append(f"n = p*q = {n}")
    debug.append(f"φ(n) = {phi}")

    e = random.randrange(3, phi - 1, 2)
    while gcd(e, phi) != 1:
        e = random.randrange(3, phi - 1, 2)

    debug.append(f"e = {e}")

    d = modinv(e, phi)
    debug.append(f"d = {d}")

    return (e, n), (d, n), p, q, phi

def encrypt_message(plaintext, public_key, debug):
    e, n = public_key
    nums = [ord(ch) for ch in plaintext]
    cipher = []

    debug.append("\n--- ENKRIPSI ---")
    for m in nums:
        c = pow(m, e, n)
        cipher.append(c)
        debug.append(f"{m}^{e} mod {n} = {c}")

    return cipher, nums

def decrypt_message(cipher, private_key, debug):
    d, n = private_key
    nums = []
    debug.append("\n--- DEKRIPSI ---")

    for c in cipher:
        m = pow(c, d, n)
        nums.append(m)
        debug.append(f"{c}^{d} mod {n} = {m}")

    plainteks = "".join(chr(x) for x in nums)
    return plainteks

# --------------------------------------------------------------------
#  GUI CLASS
# --------------------------------------------------------------------
class RSAApp:
    def __init__(self, root):
        self.root = root
        root.title("RSA Latihan 2 — Simple & Clean")
        root.geometry("1000x700")
        root.minsize(900, 600)
        root.configure(bg="#E3F2FD")

        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TFrame", background="#FAFAFA")
        style.configure("TLabel", background="#FAFAFA", font=("Segoe UI", 11))
        style.configure("TButton", font=("Segoe UI", 11, "bold"))

        main_frame = ttk.Frame(root, padding=15)
        main_frame.pack(fill="both", expand=True)

        # Title
        ttk.Label(main_frame, text="🔐 RSA ENKRIPSI — RANDOM PRIME (Simple Edition)",
                  font=("Segoe UI", 16, "bold")).pack(pady=10)

        # INPUT FRAME
        input_frame = ttk.Frame(main_frame, padding=15)
        input_frame.pack(fill="x")

        ttk.Label(input_frame, text="Plainteks:").grid(row=0, column=0, sticky="w")
        self.entry_plain = ttk.Entry(input_frame, width=60)
        self.entry_plain.grid(row=0, column=1, padx=10, pady=5)

        # Character count
        self.lbl_len = ttk.Label(input_frame, text="Length: 0 chars | 0 bytes")
        self.lbl_len.grid(row=1, column=1, sticky="w", pady=4)

        self.entry_plain.bind("<KeyRelease>", self.update_len)

        # BUTTONS
        ttk.Button(input_frame, text="Generate Key", command=self.generate_keys).grid(row=2, column=0, pady=10)
        ttk.Button(input_frame, text="Encrypt", command=self.do_encrypt).grid(row=2, column=1, sticky="w")
        ttk.Button(input_frame, text="Decrypt", command=self.do_decrypt).grid(row=2, column=1, sticky="e")

        ttk.Button(input_frame, text="Copy Cipher", command=self.copy_cipher).grid(row=3, column=0, pady=5)
        ttk.Button(input_frame, text="Clear Log", command=self.clear_log).grid(row=3, column=1, sticky="w")
        ttk.Button(input_frame, text="Reset", command=self.reset_program).grid(row=3, column=1, sticky="e")

        ttk.Button(input_frame, text="Save Debug to TXT", command=self.save_debug).grid(row=4, column=0, pady=10)

        # DEBUG AREA
        ttk.Label(main_frame, text="📘 Debug / Proses Perhitungan:").pack(anchor="w")
        self.debug_box = scrolledtext.ScrolledText(main_frame, wrap="word",
                                                   height=22, bg="#FFFFFF", fg="black")
        self.debug_box.pack(fill="both", expand=True)

        # INTERNAL
        self.public_key = None
        self.private_key = None
        self.last_cipher = None

        # Output ASCII/HEX
        self.ascii_hex_win = None

    # ---------------- UTILS -----------------
    def log(self, text):
        self.debug_box.insert(tk.END, text + "\n")
        self.debug_box.see(tk.END)

    def clear_log(self):
        self.debug_box.delete("1.0", tk.END)

    def update_len(self, event=None):
        text = self.entry_plain.get()
        self.lbl_len.config(text=f"Length: {len(text)} chars | {len(text.encode())} bytes")

    def reset_program(self):
        self.entry_plain.delete(0, tk.END)
        self.clear_log()
        self.public_key = None
        self.private_key = None
        self.last_cipher = None
        self.lbl_len.config(text="Length: 0 chars | 0 bytes")

    def copy_cipher(self):
        if not self.last_cipher:
            messagebox.showwarning("Warning", "Belum ada cipher!")
            return
        cipher_str = " ".join(map(str, self.last_cipher))
        self.root.clipboard_clear()
        self.root.clipboard_append(cipher_str)
        messagebox.showinfo("Copied", "Cipher berhasil disalin ke clipboard.")

    def save_debug(self):
        data = self.debug_box.get("1.0", tk.END)
        if data.strip() == "":
            messagebox.showwarning("Warning", "Log kosong!")
            return

        file = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Text Files", "*.txt")])
        if file:
            with open(file, "w") as f:
                f.write(data)
            messagebox.showinfo("Saved", "Debug berhasil disimpan.")

    # ---------------- RSA LOGIC -----------------
    def generate_keys(self):
        self.clear_log()
        debug = []

        pub, priv, p, q, phi = generate_keypair_random(50, 200, debug)
        self.public_key = pub
        self.private_key = priv

        for line in debug:
            self.log(line)

        self.log("\nPublic key: " + str(pub))
        self.log("Private key: " + str(priv))

    def do_encrypt(self):
        if not self.public_key:
            messagebox.showwarning("Error", "Generate key dulu!")
            return

        plaintext = self.entry_plain.get()

        # ASCII validation
        if any(ord(ch) > 126 for ch in plaintext):
            messagebox.showwarning("Error", "Input hanya boleh karakter ASCII.")
            return

        debug = []
        cipher, nums_ascii = encrypt_message(plaintext, self.public_key, debug)
        self.last_cipher = cipher

        for line in debug:
            self.log(line)

        self.log("\nCipher = " + str(cipher))

        # Show extra info: ASCII & HEX
        hex_values = " ".join(format(x, "02X") for x in nums_ascii)
        ascii_str = str(nums_ascii)

        self.log("\nASCII : " + ascii_str)
        self.log("HEX    : " + hex_values)

    def do_decrypt(self):
        if not self.private_key:
            messagebox.showwarning("Error", "Generate key dulu!")
            return
        if not self.last_cipher:
            messagebox.showwarning("Error", "Belum ada cipher!")
            return

        debug = []
        plaintext = decrypt_message(self.last_cipher, self.private_key, debug)

        for line in debug:
            self.log(line)

        self.log("\nHasil Dekripsi = " + plaintext)

# --------------------------------------------------------------------
#  RUN APP
# --------------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = RSAApp(root)
    root.mainloop()
