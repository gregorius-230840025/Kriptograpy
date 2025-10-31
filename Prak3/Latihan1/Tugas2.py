import tkinter as tk
from tkinter import ttk, messagebox

def konversi():
    oktal = entry_oktal.get()
    try:
        desimal = int(oktal, 8)
        hasil_desimal.set(str(desimal))
        hasil_biner.set(bin(desimal).replace("0b", ""))
        hasil_heksa.set(hex(desimal).replace("0x", "").upper())
    except ValueError:
        messagebox.showerror("Error", "Masukkan bilangan oktal yang valid (0-7)!")

def reset():
    entry_oktal.delete(0, tk.END)
    hasil_desimal.set("")
    hasil_biner.set("")
    hasil_heksa.set("")

root = tk.Tk()
root.title("Konversi Oktal ke Desimal, Biner, dan Heksadesimal")
root.geometry("480x400")
root.configure(bg="#20232A")

style = ttk.Style()
style.configure("TLabel", background="#20232A", foreground="white", font=("Segoe UI", 11))
style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)

judul = tk.Label(root, text="Konversi Oktal ke Desimal, Biner & Heksadesimal",
                 font=("Segoe UI", 14, "bold"), bg="#20232A", fg="#61DAFB")
judul.pack(pady=15)

frame_input = ttk.Frame(root)
frame_input.pack(pady=10)
ttk.Label(frame_input, text="Masukkan Bilangan Oktal:").grid(row=0, column=0, padx=5, pady=5)
entry_oktal = ttk.Entry(frame_input, width=25)
entry_oktal.grid(row=0, column=1, padx=5, pady=5)

frame_tombol = ttk.Frame(root)
frame_tombol.pack(pady=10)
ttk.Button(frame_tombol, text="Konversi", command=konversi).grid(row=0, column=0, padx=10)
ttk.Button(frame_tombol, text="Reset", command=reset).grid(row=0, column=1, padx=10)

frame_hasil = ttk.Frame(root)
frame_hasil.pack(pady=10)
hasil_desimal = tk.StringVar()
hasil_biner = tk.StringVar()
hasil_heksa = tk.StringVar()

ttk.Label(frame_hasil, text="Desimal:").grid(row=0, column=0, padx=5, pady=5)
ttk.Entry(frame_hasil, textvariable=hasil_desimal, width=25, state="readonly").grid(row=0, column=1, padx=5, pady=5)
ttk.Label(frame_hasil, text="Biner:").grid(row=1, column=0, padx=5, pady=5)
ttk.Entry(frame_hasil, textvariable=hasil_biner, width=25, state="readonly").grid(row=1, column=1, padx=5, pady=5)
ttk.Label(frame_hasil, text="Heksadesimal:").grid(row=2, column=0, padx=5, pady=5)
ttk.Entry(frame_hasil, textvariable=hasil_heksa, width=25, state="readonly").grid(row=2, column=1, padx=5, pady=5)

root.mainloop()
