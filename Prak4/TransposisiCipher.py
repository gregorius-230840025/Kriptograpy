# === Fungsi Substitusi Cipher ===
def substitusi_cipher(plaintext, aturan):
    ciphertext = ''
    for char in plaintext.upper():
        if char in aturan:
            ciphertext += aturan[char]
        else:
            ciphertext += char  # spasi atau karakter lain tidak berubah
    return ciphertext


# === Fungsi Transposisi Cipher (4 blok) ===
def transposisi_cipher(plaintext):
    part_length = len(plaintext) // 4
    parts = [plaintext[i:i + part_length] for i in range(0, len(plaintext), part_length)]

    print("\n=== PEMBENTUKAN BLOK TRANSPOSISI ===")
    for i, part in enumerate(parts):
        print(f"Blok {i + 1}: '{part}'")

    ciphertext = ""
    for col in range(4):
        for part in parts:
            if col < len(part):
                print(f"Menambahkan '{part[col]}' dari Blok {parts.index(part) + 1} ke ciphertext.")
                ciphertext += part[col]
    return ciphertext


# === PROGRAM UTAMA ===
def main():
    print("=== PROGRAM GABUNGAN SUBSTITUSI + TRANSPOSISI CIPHER ===")

    # Input plaintext
    plaintext = input("Masukkan plaintext: ").upper()

    # Input aturan substitusi
    print("\nMasukkan aturan substitusi (contoh: A=B berarti A diganti jadi B)")
    print("Ketik 'selesai' jika sudah selesai memasukkan aturan.\n")

    aturan_substitusi = {}
    while True:
        pasangan = input("Aturan (contoh A=B): ").strip().upper()
        if pasangan == "SELESAI":
            break
        if "=" in pasangan and len(pasangan.split("=")) == 2:
            asal, ganti = pasangan.split("=")
            asal, ganti = asal.strip(), ganti.strip()
            if len(asal) == 1 and len(ganti) == 1:
                aturan_substitusi[asal] = ganti
            else:
                print("⚠️  Gunakan hanya 1 huruf per sisi! Contoh: A=B")
        else:
            print("⚠️  Format salah! Gunakan tanda '=' di antara huruf.")

    # Proses substitusi
    cipher_subs = substitusi_cipher(plaintext, aturan_substitusi)

    # Proses transposisi
    cipher_final = transposisi_cipher(cipher_subs)

    # Tampilkan hasil akhir
    print("\n=== HASIL ENKRIPSI ===")
    print(f"Plaintext: {plaintext}")
    print(f"Ciphertext Substitusi: {cipher_subs}")
    print(f"Ciphertext Substitusi + Transposisi: {cipher_final}")


# Jalankan program
if __name__ == "__main__":
    main()
