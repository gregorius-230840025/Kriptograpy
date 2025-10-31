import itertools

# === FUNGSI FAKTORIAL ===
def faktorial(x):
    if x == 0 or x == 1:
        return 1
    hasil = 1
    for i in range(2, x + 1):
        hasil *= i
    return hasil

# === FUNGSI KOMBINASI ===
def kombinasi(n, r):
    if r > n:
        return 0
    faktorial_n = faktorial(n)
    faktorial_r = faktorial(r)
    faktorial_n_r = faktorial(n - r)
    return faktorial_n // (faktorial_r * faktorial_n_r)

# === PROGRAM UTAMA ===
def main():
    print("=== PROGRAM KOMBINASI DENGAN INISIAL HURUF ===")
    n = int(input("Masukkan jumlah total objek (n): "))
    r = int(input("Masukkan jumlah objek yang dipilih (r): "))

    # Validasi
    if r > n or n <= 0 or r <= 0:
        print("Input tidak valid! Pastikan n >= r dan keduanya lebih dari 0.")
        return

    # Buat daftar huruf (A, B, C, D, ...)
    huruf = [chr(65 + i) for i in range(n)]

    # Hitung jumlah kombinasi
    jumlah = kombinasi(n, r)

    # Buat semua kombinasi aktual menggunakan itertools
    hasil_kombinasi = list(itertools.combinations(huruf, r))

    # Tampilkan hasil
    print(f"\nJumlah kombinasi C({n}, {r}) = {jumlah}")
    print(f"Daftar kombinasi dari {huruf}:")
    for i, item in enumerate(hasil_kombinasi, 1):
        print(f"{i}. {item}")

# Jalankan program
if __name__ == "__main__":
    main()
