# === FUNGSI UTAMA SUBSTITUSI CIPHER ===
def substitusi_cipher(plaintext, aturan):
    ciphertext = ''
    for char in plaintext.upper():
        if char in aturan:
            ciphertext += aturan[char]
        else:
            ciphertext += char  # spasi/tanda baca tidak diubah
    return ciphertext

# === PROGRAM UTAMA ===
def main():
    print("=== PROGRAM SUBSTITUSI CIPHER DINAMIS ===")

    # Input plaintext
    plaintext = input("Masukkan plaintext (teks asli): ").upper()

    # Input aturan substitusi
    print("\nMasukkan aturan substitusi (contoh: A=B berarti A diganti menjadi B)")
    print("Ketik 'selesai' jika sudah selesai menambahkan aturan.\n")

    aturan_substitusi = {}
    while True:
        pasangan = input("Masukkan aturan (contoh A=B): ").strip().upper()
        if pasangan == "SELESAI":
            break
        if "=" in pasangan and len(pasangan.split("=")) == 2:
            asal, ganti = pasangan.split("=")
            asal, ganti = asal.strip(), ganti.strip()
            if len(asal) == 1 and len(ganti) == 1:
                aturan_substitusi[asal] = ganti
            else:
                print("⚠️  Format salah! Gunakan hanya 1 huruf per sisi (contoh: A=B).")
        else:
            print("⚠️  Format salah! Gunakan tanda '=' di antara huruf.")

    # Tampilkan aturan yang digunakan
    print("\nAturan substitusi yang digunakan:")
    for k, v in aturan_substitusi.items():
        print(f"{k} → {v}")

    # Enkripsi teks
    ciphertext = substitusi_cipher(plaintext, aturan_substitusi)

    # Tampilkan hasil
    print("\n=== HASIL ENKRIPSI ===")
    print(f"Plaintext : {plaintext}")
    print(f"Ciphertext: {ciphertext}")

# Jalankan program
if __name__ == "__main__":
    main()
