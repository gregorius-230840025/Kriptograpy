import tkinter as tk
from tkinter import ttk, messagebox

def konversi():
    heksa = entry_heksa.get()
    try:
        desimal = int(heksa, 16)
        hasil_desimal.set(str(desimal))
        hasil_biner.set(bin(desimal).replace("0b", ""))
        hasil_oktal.set(oct(desimal).replace("0o", ""))
    except ValueError:
        messagebox.showerror("Error", "Masukkan bilangan heksadesimal yang valid (0-9, A-F)!")

def reset():
    entry_heksa.delete(0, tk.END)
    hasil_desimal.set("")
    hasil_biner.set("")
    hasil_oktal.set("")

root = tk.Tk()
root.title("Konversi Heksadesimal ke Desimal, Biner, dan Oktal")
root.geometry("480x400")
root.configure(bg="#20232A")

style = ttk.Style()
style.configure("TLabel", background="#20232A", foreground="white", font=("Segoe UI", 11))
style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)

judul = tk.Label(root, text="Konversi Heksadesimal ke Desimal, Biner & Oktal",
                 font=("Segoe UI", 14, "bold"), bg="#20232A", fg="#61DAFB")
judul.pack(pady=15)

frame_input = ttk.Frame(root)
frame_input.pack(pady=10)
ttk.Label(frame_input, text="Masukkan Bilangan Heksadesimal:").grid(row=0, column=0, padx=5, pady=5)
entry_heksa = ttk.Entry(frame_input, width=25)
entry_heksa.grid(row=0, column=1, padx=5, pady=5)

frame_tombol = ttk.Frame(root)
frame_tombol.pack(pady=10)
ttk.Button(frame_tombol, text="Konversi", command=konversi).grid(row=0, column=0, padx=10)
ttk.Button(frame_tombol, text="Reset", command=reset).grid(row=0, column=1, padx=10)

frame_hasil = ttk.Frame(root)
frame_hasil.pack(pady=10)
hasil_desimal = tk.StringVar()
hasil_biner = tk.StringVar()
hasil_oktal = tk.StringVar()

ttk.Label(frame_hasil, text="Desimal:").grid(row=0, column=0, padx=5, pady=5)
ttk.Entry(frame_hasil, textvariable=hasil_desimal, width=25, state="readonly").grid(row=0, column=1, padx=5, pady=5)
ttk.Label(frame_hasil, text="Biner:").grid(row=1, column=0, padx=5, pady=5)
ttk.Entry(frame_hasil, textvariable=hasil_biner, width=25, state="readonly").grid(row=1, column=1, padx=5, pady=5)
ttk.Label(frame_hasil, text="Oktal:").grid(row=2, column=0, padx=5, pady=5)
ttk.Entry(frame_hasil, textvariable=hasil_oktal, width=25, state="readonly").grid(row=2, column=1, padx=5, pady=5)

root.mainloop()
