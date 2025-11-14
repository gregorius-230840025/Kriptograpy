import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from textwrap import wrap

# ---------------------------
# DES TABLES (standard)
# ---------------------------
PC1 = [
    57,49,41,33,25,17,9,
    1,58,50,42,34,26,18,
    10,2,59,51,43,35,27,
    19,11,3,60,52,44,36,
    63,55,47,39,31,23,15,
    7,62,54,46,38,30,22,
    14,6,61,53,45,37,29,
    21,13,5,28,20,12,4
]

PC2 = [
    14,17,11,24,1,5,
    3,28,15,6,21,10,
    23,19,12,4,26,8,
    16,7,27,20,13,2,
    41,52,31,37,47,55,
    30,40,51,45,33,48,
    44,49,39,56,34,53,
    46,42,50,36,29,32
]

IP = [
    58,50,42,34,26,18,10,2,
    60,52,44,36,28,20,12,4,
    62,54,46,38,30,22,14,6,
    64,56,48,40,32,24,16,8,
    57,49,41,33,25,17,9,1,
    59,51,43,35,27,19,11,3,
    61,53,45,37,29,21,13,5,
    63,55,47,39,31,23,15,7
]

IP_INV = [
    40,8,48,16,56,24,64,32,
    39,7,47,15,55,23,63,31,
    38,6,46,14,54,22,62,30,
    37,5,45,13,53,21,61,29,
    36,4,44,12,52,20,60,28,
    35,3,43,11,51,19,59,27,
    34,2,42,10,50,18,58,26,
    33,1,41,9,49,17,57,25
]

E = [
    32,1,2,3,4,5,4,5,
    6,7,8,9,8,9,10,11,
    12,13,12,13,14,15,16,17,
    16,17,18,19,20,21,20,21,
    22,23,24,25,24,25,26,27,
    28,29,28,29,30,31,32,1
]

P = [
    16,7,20,21,29,12,28,17,
    1,15,23,26,5,18,31,10,
    2,8,24,14,32,27,3,9,
    19,13,30,6,22,11,4,25
]

SHIFTS = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]

S_BOXES = [
    # S1
    [
        [14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
        [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
        [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
        [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13],
    ],
    # S2
    [
        [15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
        [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
        [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
        [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9],
    ],
    # S3
    [
        [10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
        [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
        [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
        [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12],
    ],
    # S4
    [
        [7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
        [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
        [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
        [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14],
    ],
    # S5
    [
        [2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
        [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
        [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
        [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3],
    ],
    # S6
    [
        [12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
        [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
        [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
        [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13],
    ],
    # S7
    [
        [4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
        [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
        [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
        [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12],
    ],
    # S8
    [
        [13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
        [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
        [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
        [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11],
    ],
]

# ---------------------------
# Utilities
# ---------------------------
def str_to_bin(s):
    return ''.join(f"{ord(c):08b}" for c in s)

def permute(bits, table):
    return ''.join(bits[i-1] for i in table)

def left_shift(bits, n):
    return bits[n:] + bits[:n]

def xor_bits(a, b):
    return ''.join('1' if x!=y else '0' for x,y in zip(a,b))

def sbox_substitution(bits48):
    parts = wrap(bits48, 6)
    out32 = ''
    details = []
    for i, part in enumerate(parts):
        row = int(part[0] + part[-1], 2)
        col = int(part[1:5], 2)
        val = S_BOXES[i][row][col]
        bits4 = f"{val:04b}"
        out32 += bits4
        details.append((i+1, part, row, col, val, bits4))
    return out32, details

# ---------------------------
# GUI and process
# ---------------------------
def generate_des_full():
    output.delete(1.0, tk.END)
    plaintext = entry_plain.get()
    key = entry_key.get()

    if len(key) == 0 or len(key) > 8:
        messagebox.showerror("Error", "Kunci harus 1–8 karakter.")
        return

    # pad key to 8 chars (space)
    if len(key) < 8:
        key = key + ' ' * (8 - len(key))
    key_bin = str_to_bin(key)
    output.insert(tk.END, "=== KEY (ASCII -> BIN) ===\n")
    for ch, b in zip(key, wrap(key_bin, 8)):
        output.insert(tk.END, f"'{ch}' -> {b}\n")
    output.insert(tk.END, "\nKey 64-bit: " + key_bin + "\n\n")

    # PC-1
    permuted = permute(key_bin, PC1)
    C = permuted[:28]
    D = permuted[28:]
    output.insert(tk.END, "=== PC-1 ===\n")
    output.insert(tk.END, f"PC-1 output (56-bit): {permuted}\n")
    output.insert(tk.END, f"C0: {C}\nD0: {D}\n\n")

    Cs = [C]
    Ds = [D]
    # shifts
    output.insert(tk.END, "=== LEFT SHIFTS & C/D rounds ===\n")
    for i, s in enumerate(SHIFTS, start=1):
        C = left_shift(Cs[-1], s)
        D = left_shift(Ds[-1], s)
        Cs.append(C)
        Ds.append(D)
        output.insert(tk.END, f"Round {i}: shift={s}\n")
        output.insert(tk.END, f" C{i}: {C}\n D{i}: {D}\n\n")

    # PC-2 -> subkeys
    output.insert(tk.END, "=== PC-2 -> SUBKEYS K1..K16 ===\n")
    subkeys = []
    for i in range(1,17):
        combined = Cs[i] + Ds[i]
        Ki = permute(combined, PC2)
        subkeys.append(Ki)
        output.insert(tk.END, f"K{i} (bin): {Ki}\n")
        output.insert(tk.END, f"K{i} (hex): {hex(int(Ki,2))[2:].upper().zfill(12)}\n\n")

    # Plaintext processing (padding)
    output.insert(tk.END, "=== PLAINTEXT -> BIN (with PKCS#7-like padding 0x00) ===\n")
    if plaintext == "":
        messagebox.showerror("Error", "Masukkan plaintext.")
        return
    plain_bin = ''.join(f"{ord(c):08b}" for c in plaintext)
    # pad with zeros to multiple of 64
    if len(plain_bin) % 64 != 0:
        pad_len = 64 - (len(plain_bin) % 64)
        plain_bin = plain_bin + '0'*pad_len
    output.insert(tk.END, f"Plaintext bin (len {len(plain_bin)}):\n{plain_bin}\n\n")

    # process each 64-bit block
    cipher_bin_total = ''
    block_count = len(plain_bin)//64
    for bi in range(block_count):
        output.insert(tk.END, f"=== BLOCK {bi+1} ===\n")
        block = plain_bin[bi*64:(bi+1)*64]
        output.insert(tk.END, f"Block (bin): {block}\n")
        # IP
        ip_out = permute(block, IP)
        L = ip_out[:32]
        R = ip_out[32:]
        output.insert(tk.END, f"After IP: {ip_out}\nL0: {L}\nR0: {R}\n\n")

        # 16 rounds
        Ls = [L]
        Rs = [R]
        for r in range(16):
            Ki = subkeys[r]
            output.insert(tk.END, f"--- Round {r+1} ---\n")
            output.insert(tk.END, f"K{r+1}: {Ki}\n")
            # E expansion
            eR = permute(Rs[-1], E)
            output.insert(tk.END, f"E(R): {eR}\n")
            # XOR
            xr = xor_bits(eR, Ki)
            output.insert(tk.END, f"E(R) xor K{r+1}: {xr}\n")
            # S-box
            s_out, s_det = sbox_substitution(xr)
            for det in s_det:
                box, inp, row, col, val, bits4 = det
                output.insert(tk.END, f" S{box}: in={inp} row={row} col={col} -> {val} -> {bits4}\n")
            output.insert(tk.END, f"S-box output (32): {s_out}\n")
            # P permutation
            p_out = permute(s_out, P)
            output.insert(tk.END, f"P(S): {p_out}\n")
            # XOR with L
            newR = xor_bits(Ls[-1], p_out)
            newL = Rs[-1]
            output.insert(tk.END, f"L{r+1}: {newL}\nR{r+1}: {newR}\n\n")
            Ls.append(newL)
            Rs.append(newR)

        preoutput = Rs[-1] + Ls[-1]
        output.insert(tk.END, f"Preoutput (R16||L16): {preoutput}\n")
        cipher_block = permute(preoutput, IP_INV)
        output.insert(tk.END, f"After IP^-1 (cipher block): {cipher_block}\n\n")
        cipher_bin_total += cipher_block

    cipher_hex = hex(int(cipher_bin_total, 2))[2:].upper()
    output.insert(tk.END, "=== FINAL CIPHER ===\n")
    output.insert(tk.END, f"Cipher (bin): {cipher_bin_total}\n")
    output.insert(tk.END, f"Cipher (hex): {cipher_hex}\n")

# ---------------------------
# Build GUI
# ---------------------------
root = tk.Tk()
root.title("DES Visualizer (Verbose)")
root.geometry("900x700")
root.resizable(True, True)

frame = ttk.Frame(root, padding=8)
frame.pack(fill='x')

ttk.Label(frame, text="Plaintext: ").grid(row=0, column=0, sticky='w')
entry_plain = ttk.Entry(frame, width=70)
entry_plain.grid(row=0, column=1, padx=6, pady=6, sticky='w')

ttk.Label(frame, text="Key (max 8 chars): ").grid(row=1, column=0, sticky='w')
entry_key = ttk.Entry(frame, width=30)
entry_key.grid(row=1, column=1, padx=6, pady=6, sticky='w')

btn = ttk.Button(frame, text="Encrypt & Show Steps", command=generate_des_full)
btn.grid(row=0, column=2, rowspan=2, padx=6, sticky='ns')

output = scrolledtext.ScrolledText(root, wrap='none', font=("Consolas", 10))
output.pack(fill='both', expand=True, padx=6, pady=6)

root.mainloop()
