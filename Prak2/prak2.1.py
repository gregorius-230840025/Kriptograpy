import tkinter as tk
from tkinter import messagebox

def buka_kalkulator():
    kalkulator = tk.Toplevel(root)
    kalkulator.title("Kalkulator Sederhana")
    kalkulator.geometry("400x300")
    kalkulator.config(bg="#e0f0f2")

    tk.Label(kalkulator, text="=== Kalkulator Sederhana ===", font=("Arial", 12, "bold"), bg="#e0f0f2").pack(pady=10)

    tk.Label(kalkulator, text="Nilai A:", bg="#e0f0f2").pack()
    entry_a = tk.Entry(kalkulator)
    entry_a.pack(pady=5)

    tk.Label(kalkulator, text="Nilai B:", bg="#e0f0f2").pack()
    entry_b = tk.Entry(kalkulator)
    entry_b.pack(pady=5)

    tk.Label(kalkulator, text="Operator (+, -, *, /):", bg="#e0f0f2").pack()
    entry_op = tk.Entry(kalkulator)
    entry_op.pack(pady=5)

    def hitung():
        try:
            a = float(entry_a.get())
            b = float(entry_b.get())
            op = entry_op.get()

            if op == '+':
                hasil = a + b
            elif op == '-':
                hasil = a - b
            elif op == '*':
                hasil = a * b
            elif op == '/':
                hasil = a / b if b != 0 else "Tidak bisa dibagi 0"
            else:
                hasil = "Operator tidak dikenal!"

            lanjut = messagebox.askquestion("Hasil", f"Hasil: {hasil}\n\nHitung lagi?")
            if lanjut == "yes":
                entry_a.delete(0, tk.END)
                entry_b.delete(0, tk.END)
                entry_op.delete(0, tk.END)
                entry_a.focus()
            else:
                kalkulator.destroy()

        except ValueError:
            messagebox.showerror("Error", "Masukkan angka yang valid!")

    tk.Button(kalkulator, text="Hitung", command=hitung).pack(pady=15)

# === Menu Utama ===
root = tk.Tk()
root.title("Menu Utama Program IF & Kalkulator")
root.geometry("400x300")
root.config(bg="#dbe5e6")

tk.Label(root, text="=== MENU UTAMA ===", font=("Arial", 14, "bold"), bg="#dbe5e6").pack(pady=20)
tk.Button(root, text="Kalkulator Sederhana", width=30, command=buka_kalkulator).pack(pady=10)
tk.Button(root, text="Keluar", width=30, command=root.destroy).pack(pady=20)

root.mainloop()
