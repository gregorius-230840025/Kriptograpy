def kalkulator_hybrid():
    print("=== Kalkulator Hybrid ===")
    ekspresi = input("Masukkan ekspresi matematika: ")

    try:
        # Hapus spasi agar bisa memproses ekspresi dengan atau tanpa spasi
        ekspresi_bersih = ekspresi.replace(" ", "")

        # Evaluasi hasil ekspresi
        hasil = eval(ekspresi_bersih)

        print(f"Ekspresi Diterima : {ekspresi}")
        print(f"Hasil Diproses   : {ekspresi_bersih}")
        print(f"Output (Hasil)   > {hasil}")
    except Exception as e:
        print("Terjadi kesalahan dalam perhitungan!")
        print("Pesan error:", e)


# Jalankan program
kalkulator_hybrid()
