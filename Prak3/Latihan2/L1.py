import itertools

# === 1. Permutasi Menyeluruh ===
def permutasi_menyeluruh(arr):
    return list(itertools.permutations(arr))

# === 2. Permutasi Sebagian ===
def permutasi_sebagian(arr, k):
    return list(itertools.permutations(arr, k))

# === 3. Permutasi Keliling ===
def permutasi_keliling(arr):
    if len(arr) == 1:
        return [arr]
    pertama = arr[0]
    permutasi_penuh = list(itertools.permutations(arr[1:]))
    return [[pertama] + list(perm) for perm in permutasi_penuh]

# === 4. Permutasi Berkelompok ===
def permutasi_berkelompok(grup):
    hasil = [[]]
    for kelompok in grup:
        hasil_baru = []
        for hsl in hasil:
            for perm in itertools.permutations(kelompok):
                hasil_baru.append(hsl + list(perm))
        hasil = hasil_baru
    return hasil

# === MENU UTAMA ===
def main():
    print("=== PROGRAM PERMUTASI PYTHON ===")
    print("1. Permutasi Menyeluruh")
    print("2. Permutasi Sebagian")
    print("3. Permutasi Keliling")
    print("4. Permutasi Data Berkelompok")
    pilihan = int(input("Pilih jenis permutasi (1-4): "))

    if pilihan == 1:
        data = input("Masukkan elemen (pisahkan dengan spasi): ").split()
        hasil = permutasi_menyeluruh(data)

    elif pilihan == 2:
        data = input("Masukkan elemen (pisahkan dengan spasi): ").split()
        k = int(input("Masukkan panjang permutasi (k): "))
        hasil = permutasi_sebagian(data, k)

    elif pilihan == 3:
        data = input("Masukkan elemen (pisahkan dengan spasi): ").split()
        hasil = permutasi_keliling(data)

    elif pilihan == 4:
        n = int(input("Masukkan jumlah kelompok: "))
        grup = []
        for i in range(n):
            anggota = input(f"Masukkan elemen kelompok {i+1} (pisahkan spasi): ").split()
            grup.append(anggota)
        hasil = permutasi_berkelompok(grup)

    else:
        print("Pilihan tidak valid!")
        return

    print("\n=== HASIL PERMUTASI ===")
    for i, h in enumerate(hasil, 1):
        print(f"{i}: {h}")
    print(f"\nTotal permutasi: {len(hasil)}")

# Jalankan program
if __name__ == "__main__":
    main()
