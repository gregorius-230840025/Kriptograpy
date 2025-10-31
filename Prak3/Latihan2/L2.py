import itertools

def atur_buku_di_rak(n, r):
    rak = [f"Rak-{i+1}" for i in range(r)]
    # Buat semua kombinasi penempatan buku
    hasil = list(itertools.product(rak, repeat=n))
    return hasil

def main():
    print("=== PROGRAM PENGATURAN BUKU DI RAK ===")
    n = int(input("Masukkan jumlah buku (n): "))
    r = int(input("Masukkan jumlah bagian rak (r): "))

    hasil = atur_buku_di_rak(n, r)

    print(f"\n=== Semua cara mengatur {n} buku di {r} rak ===")
    for i, h in enumerate(hasil, 1):
        print(f"{i}: {h}")
    print(f"\nTotal cara: {len(hasil)}")

if __name__ == "__main__":
    main()
