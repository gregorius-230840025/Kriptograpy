import tkinter as tk
from tkinter import messagebox

# === Fungsi masing-masing latihan ===

def latihan1():
    # If Tunggal
    window = tk.Toplevel(root)
    window.title("Latihan 1 - If Tunggal")
    window.geometry("400x250")
    window.config(bg="#e0f0f2")

    tk.Label(window, text="=== If Tunggal ===", font=("Arial", 12, "bold"), bg="#e0f0f2").pack(pady=10)
    tk.Label(window, text="Masukkan suhu:", bg="#e0f0f2").pack()
    suhu = tk.Entry(window)
    suhu.pack(pady=5)

    def cek_suhu():
        try:
            t = float(suhu.get())
            if t > 25:
                pesan = "Cuaca panas, nyalakan AC"
            else:
                pesan = "Cuaca sejuk, tidak perlu AC"
            messagebox.showinfo("Hasil", pesan)
        except ValueError:
            messagebox.showerror("Error", "Masukkan angka yang valid!")

    tk.Button(window, text="Cek Suhu", command=cek_suhu).pack(pady=10)


def latihan2():
    # If-Else
    window = tk.Toplevel(root)
    window.title("Latihan 2 - If Else")
    window.geometry("400x250")
    window.config(bg="#e0f0f2")

    tk.Label(window, text="=== If - Else ===", font=("Arial", 12, "bold"), bg="#e0f0f2").pack(pady=10)
    tk.Label(window, text="Masukkan password:", bg="#e0f0f2").pack()
    pw = tk.Entry(window, show="*")
    pw.pack(pady=5)

    def cek_password():
        if pw.get() == "secret":
            messagebox.showinfo("Akses", "Akses diterima")
        else:
            messagebox.showwarning("Akses", "Akses ditolak")

    tk.Button(window, text="Periksa", command=cek_password).pack(pady=10)


def latihan3():
    # If-Elif-Else
    window = tk.Toplevel(root)
    window.title("Latihan 3 - If Elif Else")
    window.geometry("400x300")
    window.config(bg="#e0f0f2")

    tk.Label(window, text="=== If - Elif - Else ===", font=("Arial", 12, "bold"), bg="#e0f0f2").pack(pady=10)
    tk.Label(window, text="Masukkan nilai:", bg="#e0f0f2").pack()
    nilai = tk.Entry(window)
    nilai.pack(pady=5)

    def cek_nilai():
        try:
            n = float(nilai.get())
            if n >= 90:
                hasil = "Anda mendapat nilai A"
            elif n >= 80:
                hasil = "Anda mendapat nilai B"
            elif n >= 70:
                hasil = "Anda mendapat nilai C"
            else:
                hasil = "Perbaiki Nilai"
            messagebox.showinfo("Hasil", hasil)
        except ValueError:
            messagebox.showerror("Error", "Masukkan angka yang valid!")

    tk.Button(window, text="Cek Nilai", command=cek_nilai).pack(pady=10)


def latihan4():
    # If Bersarang
    window = tk.Toplevel(root)
    window.title("Latihan 4 - If Bersarang")
    window.geometry("400x250")
    window.config(bg="#e0f0f2")

    tk.Label(window, text="=== If Bersarang ===", font=("Arial", 12, "bold"), bg="#e0f0f2").pack(pady=10)
    tk.Label(window, text="Masukkan angka:", bg="#e0f0f2").pack()
    angka = tk.Entry(window)
    angka.pack(pady=5)

    def cek_angka():
        try:
            n = int(angka.get())
            if n > 0:
                hasil = "Angka positif\n"
                if n % 2 == 0:
                    hasil += "Angka genap"
                else:
                    hasil += "Angka ganjil"
            else:
                hasil = "Angka negatif"
            messagebox.showinfo("Hasil", hasil)
        except ValueError:
            messagebox.showerror("Error", "Masukkan angka yang valid!")

    tk.Button(window, text="Periksa Angka", command=cek_angka).pack(pady=10)


def latihan5():
    # If dengan operator logika
    window = tk.Toplevel(root)
    window.title("Latihan 5 - Operator Logika")
    window.geometry("400x300")
    window.config(bg="#e0f0f2")

    tk.Label(window, text="=== If dengan Operator Logika ===", font=("Arial", 12, "bold"), bg="#e0f0f2").pack(pady=10)
    tk.Label(window, text="Masukkan umur:", bg="#e0f0f2").pack()
    umur = tk.Entry(window)
    umur.pack(pady=5)
    tk.Label(window, text="Masukkan tinggi badan (cm):", bg="#e0f0f2").pack()
    tinggi = tk.Entry(window)
    tinggi.pack(pady=5)

    def cek_syarat():
        try:
            u = int(umur.get())
            t = int(tinggi.get())
            if u >= 18 and t >= 155:
                hasil = "Anda memenuhi syarat"
            else:
                hasil = "Anda tidak memenuhi syarat"
            messagebox.showinfo("Hasil", hasil)
        except ValueError:
            messagebox.showerror("Error", "Masukkan angka yang valid!")

    tk.Button(window, text="Cek Syarat", command=cek_syarat).pack(pady=10)


# === MENU UTAMA ===
root = tk.Tk()
root.title("Program Latihan Tkinter - IF Statement")
root.geometry("400x400")
root.config(bg="#dbe5e6")

tk.Label(root, text="=== MENU UTAMA ===", font=("Arial", 14, "bold"), bg="#dbe5e6").pack(pady=20)

tk.Button(root, text="Latihan 1 - If Tunggal", width=30, command=latihan1).pack(pady=5)
tk.Button(root, text="Latihan 2 - If Else", width=30, command=latihan2).pack(pady=5)
tk.Button(root, text="Latihan 3 - If Elif Else", width=30, command=latihan3).pack(pady=5)
tk.Button(root, text="Latihan 4 - If Bersarang", width=30, command=latihan4).pack(pady=5)
tk.Button(root, text="Latihan 5 - If dengan Operator Logika", width=30, command=latihan5).pack(pady=5)
tk.Button(root, text="Keluar", width=30, command=root.destroy).pack(pady=20)

root.mainloop()
