import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
import string

# =========================
#   KELAS VIGENERE CIPHER
# =========================
class VigenereCipher:
    def __init__(self, alphabet=string.ascii_uppercase):
        self.alphabet = alphabet

    def _normalize(self, text):
        return text.upper()

    def generate_key(self, text, key):
        text = self._normalize(text)
        key = self._normalize(key)
        if not key:
            return ""

        key_chars = list(key)
        expanded = []
        ki = 0
        for ch in text:
            if ch in self.alphabet:
                expanded.append(key_chars[ki % len(key_chars)])
                ki += 1
            else:
                expanded.append(ch)
        return "".join(expanded)

    def encrypt(self, plaintext, key):
        p = self._normalize(plaintext)
        generated_key = self.generate_key(p, key)
        ciphertext = []
        steps = []

        for i, ch in enumerate(p):
            kch = generated_key[i]
            if ch not in self.alphabet:
                ciphertext.append(ch)
                steps.append(f"'{ch}' tidak diubah (bukan huruf A-Z).")
                continue
            pi = self.alphabet.index(ch)
            ki = self.alphabet.index(kch)
            ci = (pi + ki) % len(self.alphabet)
            cch = self.alphabet[ci]
            ciphertext.append(cch)
            steps.append(f"{ch} ({pi}) + {kch} ({ki}) -> {ci} -> {cch}")
        return "".join(ciphertext), generated_key, steps

    def decrypt(self, ciphertext, key):
        c = self._normalize(ciphertext)
        generated_key = self.generate_key(c, key)
        plaintext = []
        steps = []

        for i, ch in enumerate(c):
            kch = generated_key[i]
            if ch not in self.alphabet:
                plaintext.append(ch)
                steps.append(f"'{ch}' tidak diubah (bukan huruf A-Z).")
                continue
            ci = self.alphabet.index(ch)
            ki = self.alphabet.index(kch)
            pi = (ci - ki + len(self.alphabet)) % len(self.alphabet)
            pch = self.alphabet[pi]
            plaintext.append(pch)
            steps.append(f"{ch} ({ci}) - {kch} ({ki}) -> {pi} -> {pch}")
        return "".join(plaintext), generated_key, steps


# =========================
#     KELAS GUI TKINTER
# =========================
class VigenereGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Vigenère Cipher — GUI (Tkinter)")
        self.geometry("880x560")
        self.minsize(780, 520)
        self.configure(bg="#f5f7fb")

        # Gaya ttk
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TFrame', background="#f5f7fb")
        style.configure('Title.TLabel', font=('Inter', 18, 'bold'), background="#f5f7fb")
        style.configure('TLabel', background="#f5f7fb", font=('Inter', 10))
        style.configure('Accent.TButton', font=('Inter', 10, 'bold'), padding=6)
        style.configure('TEntry', padding=5)

        self.cipher = VigenereCipher()

        self._build_ui()

    def _build_ui(self):
        # Header
        top_frame = ttk.Frame(self, padding=(18, 12))
        top_frame.pack(fill='x')
        ttk.Label(top_frame, text="Vigenère Cipher", style='Title.TLabel').pack(side='left')
        ttk.Label(top_frame, text=" — Enkripsi & Dekripsi dengan detail langkah", style='TLabel').pack(side='left', padx=(8,0))

        main = ttk.Frame(self, padding=(12,8))
        main.pack(fill='both', expand=True)

        # ====================
        # Panel Kiri (Input)
        # ====================
        left = ttk.Frame(main)
        left.pack(side='left', fill='y', padx=(0,10), pady=6)

        ttk.Label(left, text="Teks (Plaintext / Ciphertext):").pack(anchor='w', pady=(4,0))
        self.text_input = ScrolledText(left, width=40, height=8, wrap='word', font=('Inter', 10))
        self.text_input.pack(pady=(2,8))

        ttk.Label(left, text="Kunci (Key):").pack(anchor='w', pady=(4,0))
        self.key_entry = ttk.Entry(left, width=30, font=('Inter', 10))
        self.key_entry.pack(pady=(2,8))

        # Tombol Enkripsi/Dekripsi
        btn_frame = ttk.Frame(left)
        btn_frame.pack(fill='x', pady=(6,8))
        ttk.Button(btn_frame, text="Enkripsi →", style='Accent.TButton', command=self.on_encrypt).pack(side='left', padx=(0,6))
        ttk.Button(btn_frame, text="← Dekripsi", style='Accent.TButton', command=self.on_decrypt).pack(side='left', padx=(6,6))
        ttk.Button(btn_frame, text="Bersihkan", command=self.on_clear).pack(side='left', padx=(6,0))

        # ====================
        # Panel Kanan (Output)
        # ====================
        right = ttk.Frame(main)
        right.pack(side='left', fill='both', expand=True, pady=6)

        # Hasil
        res_frame = ttk.LabelFrame(right, text="Hasil", padding=(8,8))
        res_frame.pack(fill='x', padx=(0,6), pady=(0,8))

        ttk.Label(res_frame, text="Hasil (Ciphertext / Plaintext):").pack(anchor='w')
        self.result_var = tk.StringVar()
        ttk.Entry(res_frame, textvariable=self.result_var, font=('Inter', 11), width=60).pack(fill='x', pady=6, padx=(0,4))

        ttk.Label(res_frame, text="Kunci yang Digunakan (setelah perluasan):").pack(anchor='w')
        self.generated_key_var = tk.StringVar()
        ttk.Entry(res_frame, textvariable=self.generated_key_var, font=('Inter', 10), width=60).pack(fill='x', pady=6, padx=(0,4))

        # Detail langkah
        steps_frame = ttk.LabelFrame(right, text="Langkah-langkah Proses", padding=(8,8))
        steps_frame.pack(fill='both', expand=True, padx=(0,6))
        self.steps_text = ScrolledText(steps_frame, wrap='word', font=('Inter', 10), state='disabled')
        self.steps_text.pack(fill='both', expand=True)

    # ====================
    # Fungsi Tombol
    # ====================
    def on_encrypt(self):
        raw = self.text_input.get('1.0', 'end').strip()
        key = self.key_entry.get().strip()
        if not raw or not key:
            messagebox.showwarning("Input kosong", "Masukkan teks dan kunci terlebih dahulu.")
            return

        cipher_text, gen_key, steps = self.cipher.encrypt(raw, key)
        self.result_var.set(cipher_text)
        self.generated_key_var.set(gen_key)
        self._show_steps("ENKRIPSI", raw, gen_key, steps)

    def on_decrypt(self):
        raw = self.text_input.get('1.0', 'end').strip()
        key = self.key_entry.get().strip()
        if not raw or not key:
            messagebox.showwarning("Input kosong", "Masukkan teks dan kunci terlebih dahulu.")
            return

        plain_text, gen_key, steps = self.cipher.decrypt(raw, key)
        self.result_var.set(plain_text)
        self.generated_key_var.set(gen_key)
        self._show_steps("DEKRIPSI", raw, gen_key, steps)

    def _show_steps(self, title, original, key, steps):
        self.steps_text.config(state='normal')
        self.steps_text.delete('1.0', 'end')
        self.steps_text.insert('end', f"=== PROSES {title} VIGENÈRE ===\n\n")
        self.steps_text.insert('end', f"Teks yang diproses : {original}\n")
        self.steps_text.insert('end', f"Kunci (setelah perluasan) : {key}\n\n")
        self.steps_text.insert('end', "Langkah per karakter:\n")
        for i, s in enumerate(steps, start=1):
            self.steps_text.insert('end', f"{i:03d}. {s}\n")
        self.steps_text.insert('end', "\n=== SELESAI ===")
        self.steps_text.config(state='disabled')

    def on_clear(self):
        self.text_input.delete('1.0', 'end')
        self.key_entry.delete(0, 'end')
        self.result_var.set("")
        self.generated_key_var.set("")
        self.steps_text.config(state='normal')
        self.steps_text.delete('1.0', 'end')
        self.steps_text.config(state='disabled')


# =========================
#   MAIN PROGRAM
# =========================
if __name__ == "__main__":
    app = VigenereGUI()
    app.mainloop()
