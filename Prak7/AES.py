"""
AES-128 Visualizer (Python + Tkinter) — Fixed patch + Key Expansion Trace
Author: ChatGPT (GPT-5 Thinking mini)

Perbaikan:
- Memperbaiki _format_hex_rows yang rusak/duplikat.
- Memperbaiki validasi input dan penggunaan insert() dengan newline.
- Normalisasi tipe data dan safe padding/truncation.
- Menambahkan key_expansion_trace() yang menampilkan RotWord/SubWord/Rcon/XOR per-word.
- Memastikan UI dapat berjalan tanpa SyntaxError.
"""

import tkinter as tk
from tkinter import ttk, messagebox

# S-Box and helpers (same as before)
SBOX = [
    0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76,
    0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0,
    0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15,
    0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75,
    0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84,
    0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf,
    0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8,
    0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2,
    0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73,
    0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb,
    0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79,
    0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08,
    0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a,
    0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e,
    0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf,
    0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16,
]

RCON = [0x00,0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1B,0x36]


# ---- AES core utilities ----
def bytes_to_state(b):
    arr = list(b)
    arr = (arr + [0]*16)[:16]
    # state is 4 rows x 4 cols (row-major here where state[r][c] = arr[r + 4*c])
    return [[arr[r + 4*c] for c in range(4)] for r in range(4)]


def state_to_bytes(s):
    out = []
    for c in range(4):
        for r in range(4):
            out.append(s[r][c] & 0xFF)
    return out


def xor_bytes(a, b):
    a_l = (list(a) + [0]*16)[:16]
    b_l = (list(b) + [0]*16)[:16]
    return [x ^ y for x, y in zip(a_l, b_l)]


def sub_bytes(state):
    return [[SBOX[byte & 0xFF] for byte in row] for row in state]


def shift_rows(state):
    s = [row[:] for row in state]
    # shift left per row index
    for r in range(4):
        s[r] = s[r][r:] + s[r][:r]
    return s


def mul(a, b):
    res = 0
    for i in range(8):
        if b & 1:
            res ^= a
        hi = a & 0x80
        a = (a << 1) & 0xFF
        if hi:
            a ^= 0x1B
        b >>= 1
    return res & 0xFF


def mix_single_column(col):
    a = col[:]
    return [
        (mul(a[0], 2) ^ mul(a[1], 3) ^ a[2] ^ a[3]) & 0xFF,
        (a[0] ^ mul(a[1], 2) ^ mul(a[2], 3) ^ a[3]) & 0xFF,
        (a[0] ^ a[1] ^ mul(a[2], 2) ^ mul(a[3], 3)) & 0xFF,
        (mul(a[0], 3) ^ a[1] ^ a[2] ^ mul(a[3], 2)) & 0xFF,
    ]


def mix_columns(state):
    out = [[0] * 4 for _ in range(4)]
    for c in range(4):
        col = [state[r][c] for r in range(4)]
        mixed = mix_single_column(col)
        for r in range(4):
            out[r][c] = mixed[r]
    return out


def add_round_key(state, round_key):
    st_bytes = state_to_bytes(state)
    rk_bytes = (list(round_key) + [0] * 16)[:16]
    x = xor_bytes(st_bytes, rk_bytes)
    return bytes_to_state(x)


# Key expansion helpers
def rot_word(word):
    return word[1:] + word[:1]


def sub_word(word):
    return [SBOX[b & 0xFF] for b in word]


def xor_word(a, b):
    return [x ^ y for x, y in zip(a, b)]


# New: key_expansion_trace that returns round_keys and a trace list
def key_expansion_trace(key_bytes):
    Nk = 4
    Nr = 10
    kb = (list(key_bytes) + [0] * 16)[:16]
    w = [list(kb[i:i + 4]) for i in range(0, 16, 4)]
    trace = []
    trace.append("=== Key Expansion Trace ===")
    trace.append(f"Initial words (w0..w3):")
    for idx in range(4):
        trace.append(f"  w[{idx:02d}] = " + bytes_to_hex(w[idx]))
    trace.append("")

    for i in range(4, 4 * (Nr + 1)):
        trace.append(f"--- Compute w[{i:02d}] ---")
        temp = w[i - 1][:]
        trace.append("  temp (w[i-1]) = " + bytes_to_hex(temp))
        if i % Nk == 0:
            rot = rot_word(temp)
            trace.append("  after RotWord = " + bytes_to_hex(rot))
            sub = sub_word(rot)
            trace.append("  after SubWord = " + bytes_to_hex(sub))
            rcon_word = [RCON[i // Nk], 0x00, 0x00, 0x00]
            trace.append("  Rcon = " + bytes_to_hex(rcon_word))
            temp = xor_word(sub, rcon_word)
            trace.append("  temp after XOR with Rcon = " + bytes_to_hex(temp))
        else:
            trace.append("  (no Rot/Sub/Rcon for this i)")
        new_w = xor_word(w[i - Nk], temp)
        trace.append(f"  w[{i:02d}] = w[{i-Nk:02d}] XOR temp = " + bytes_to_hex(new_w))
        w.append(new_w)
        trace.append("")

    # build round keys (k0..k10)
    round_keys = []
    for r in range(Nr + 1):
        rk = []
        for j in range(4):
            rk += w[r * 4 + j]
        round_keys.append(rk)

    trace.append("=== Finished key expansion ===")
    return round_keys, trace


# Original key_expansion kept for compatibility (not used when trace version is called)
def key_expansion(key_bytes):
    Nk = 4
    Nr = 10
    kb = (list(key_bytes) + [0] * 16)[:16]
    w = [list(kb[i:i + 4]) for i in range(0, 16, 4)]
    for i in range(4, 4 * (Nr + 1)):
        temp = w[i - 1][:]
        if i % Nk == 0:
            temp = xor_word(sub_word(rot_word(temp)), [RCON[i // Nk], 0, 0, 0])
        w.append(xor_word(w[i - Nk], temp))
    round_keys = []
    for r in range(Nr + 1):
        rk = []
        for j in range(4):
            rk += w[r * 4 + j]
        round_keys.append(rk)
    return round_keys


# Formatting helpers
def byte_to_hex(b):
    return f"{b & 0xFF:02X}"


def state_to_hex(state):
    lines = []
    for r in range(4):
        lines.append(' '.join(byte_to_hex(b) for b in state[r]))
    return '\n'.join(lines)


def bytes_to_hex(bts):
    return ' '.join(f"{x & 0xFF:02X}" for x in bts)


# ---------------- GUI -----------------
class AESVisualizer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AES-128 Visualizer — Stepwise")
        self.geometry("1100x780")
        self.configure(bg="#0f1720")
        self.style = ttk.Style(self)
        try:
            self.style.theme_use('clam')
        except Exception:
            pass

        # State for stepwise flow
        self.plain_bytes = None
        self.key_bytes = None
        self.xor_bytes_res = None
        self.round_keys = None
        self.current_round = 0
        self.current_substep = 0
        self.current_state = bytes_to_state([0] * 16)

        self._build_ui()

    def _build_ui(self):
        header = tk.Label(self, text="AES-128 Visualizer — Langkah demi langkah", bg="#0f1720", fg="#e6eef6",
                          font=('Segoe UI', 18, 'bold'))
        header.pack(pady=(8, 6))

        top_frame = ttk.Frame(self)
        top_frame.pack(fill='x', padx=10)

        left_in = ttk.Frame(top_frame)
        left_in.pack(side='left', padx=6, pady=4, anchor='n')
        ttk.Label(left_in, text="Plaintext (16 chars):").pack(anchor='w')
        self.plain_entry = ttk.Entry(left_in, width=36, font=('Consolas', 12))
        self.plain_entry.pack(pady=2)
        ttk.Label(left_in, text="Key (16 chars):").pack(anchor='w')
        self.key_entry = ttk.Entry(left_in, width=36, font=('Consolas', 12))
        self.key_entry.pack(pady=2)

        btns = ttk.Frame(top_frame)
        btns.pack(side='left', padx=12)
        ttk.Button(btns, text="Langkah 1: Konversi → Hex & Biner", command=self.step_convert).pack(fill='x', pady=3)
        ttk.Button(btns, text="Langkah 2: XOR Plain & Key (AddRoundKey)", command=self.step_xor).pack(fill='x', pady=3)
        ttk.Button(btns, text="Langkah 3: Generate Key Schedule (Trace)", command=self.step_generate_keys).pack(fill='x', pady=3)
        ttk.Button(btns, text="Mulai Enkripsi Round 1", command=self.start_rounds).pack(fill='x', pady=3)
        ttk.Button(btns, text="Reset Semua", command=self.reset_all).pack(fill='x', pady=3)

        mid_pane = ttk.Panedwindow(self, orient='horizontal')
        mid_pane.pack(fill='both', expand=False, padx=10, pady=6)

        conv_frame = ttk.Labelframe(mid_pane, text='Konversi (Hex / Biner)', width=520)
        mid_pane.add(conv_frame)
        self.conv_plain = tk.Text(conv_frame, width=38, height=6, font=('Consolas', 14), wrap='none')
        self.conv_plain.pack(side='left', padx=4, pady=4)
        self.conv_key = tk.Text(conv_frame, width=38, height=6, font=('Consolas', 14), wrap='none')
        self.conv_key.pack(side='left', padx=4, pady=4)

        xor_frame = ttk.Labelframe(mid_pane, text='Hasil XOR / AddRoundKey (Round 0)', width=520)
        mid_pane.add(xor_frame)
        self.xor_text = tk.Text(xor_frame, width=80, height=6, font=('Consolas', 14), wrap='none')
        self.xor_text.pack(padx=4, pady=4)

        lower_pane = ttk.Panedwindow(self, orient='horizontal')
        lower_pane.pack(fill='both', expand=True, padx=10, pady=6)

        left = ttk.Frame(lower_pane, width=420)
        right = ttk.Frame(lower_pane, width=620)
        lower_pane.add(left)
        lower_pane.add(right)

        ttk.Label(left, text='Key Schedule (Round keys)', font=('Segoe UI', 12, 'bold')).pack(anchor='w')
        self.keys_list = tk.Listbox(left, height=16, font=('Consolas', 12))
        self.keys_list.pack(fill='both', expand=True, padx=4, pady=6)

        ttk.Label(left, text='Current State (4x4) — Font besar', font=('Segoe UI', 12, 'bold')).pack(anchor='w')
        self.state_text = tk.Text(left, width=36, height=8, font=('Consolas', 16, 'bold'))
        self.state_text.pack(padx=4, pady=4)

        control_frame = ttk.Frame(right)
        control_frame.pack(fill='x', padx=4, pady=4)
        ttk.Label(control_frame, text='Kontrol Enkripsi per-Substep (SubBytes → ShiftRows → MixColumns → AddRoundKey)',
                  font=('Segoe UI', 10, 'bold')).pack(anchor='w')
        h = ttk.Frame(control_frame)
        h.pack(anchor='w', pady=6)
        ttk.Button(h, text='Next Substep', command=self.next_substep).pack(side='left', padx=6)
        ttk.Button(h, text='Next Round', command=self.next_round).pack(side='left', padx=6)
        ttk.Button(h, text='Tampilkan Semua Round (Run All)', command=self.run_all_rounds).pack(side='left', padx=6)

        ttk.Label(right, text='Trace Detail (Font besar untuk tiap proses)', font=('Segoe UI', 12, 'bold')).pack(anchor='w')
        self.trace_text = tk.Text(right, width=70, height=28, font=('Consolas', 14), wrap='word')
        self.trace_text.pack(fill='both', expand=True, padx=4, pady=6)

    # ------------ Step implementations ----------------
    def _validate_ascii16(self):
        pt = self.plain_entry.get()
        k = self.key_entry.get()
        if len(pt) != 16 or len(k) != 16:
            messagebox.showerror('Input error', 'Plaintext dan Key harus tepat 16 karakter ASCII (128-bit).')
            return None
        return pt.encode('utf-8'), k.encode('utf-8')

    def _format_hex_rows(self, bts):
        # Accept bytes or list[int]; normalize to list of 16 ints
        if bts is None:
            arr = [0] * 16
        elif isinstance(bts, (bytes, bytearray)):
            arr = list(bts)
        else:
            arr = list(bts)
        if len(arr) != 16:
            arr = (arr + [0] * 16)[:16]
        s = bytes_to_state(arr)
        lines = []
        for r in range(4):
            hex_part = ' '.join(f"{x:02X}" for x in s[r])
            bin_part = ' '.join(f"{x:08b}" for x in s[r])
            lines.append(hex_part + '    ' + bin_part)
        return '\n'.join(lines)

    def step_convert(self):
        validated = self._validate_ascii16()
        if not validated:
            return
        pt, k = validated
        self.plain_bytes = list(pt)
        self.key_bytes = list(k)
        self.conv_plain.delete('1.0', 'end')
        self.conv_key.delete('1.0', 'end')

        self.conv_plain.insert('end',
                               f"Plaintext ASCII: {pt.decode()}\n\nHex + Biner (4x4 rows):\n{self._format_hex_rows(self.plain_bytes)}")
        self.conv_key.insert('end',
                             f"Key ASCII: {k.decode()}\n\nHex + Biner (4x4 rows):\n{self._format_hex_rows(self.key_bytes)}")
        self.trace_text.insert('end', '[Langkah 1] Konversi selesai — plaintext dan key ditampilkan dalam HEX dan BINER.\n\n')
        self.trace_text.see('end')

    def step_xor(self):
        # XOR plaintext with key as initial AddRoundKey (round 0)
        if self.plain_bytes is None or self.key_bytes is None:
            messagebox.showinfo('Info', 'Lakukan Langkah 1 (Konversi) terlebih dahulu.')
            return
        st = list(self.plain_bytes) if isinstance(self.plain_bytes, (list, bytes, bytearray)) else list(self.plain_bytes)
        rk = list(self.key_bytes) if isinstance(self.key_bytes, (list, bytes, bytearray)) else list(self.key_bytes)
        st = (st + [0] * 16)[:16]
        rk = (rk + [0] * 16)[:16]
        self.xor_bytes_res = xor_bytes(st, rk)
        self.xor_text.delete('1.0', 'end')
        self.xor_text.insert('end', f"Result (HEX):\n{bytes_to_hex(self.xor_bytes_res)}\n\nAs 4x4:\n{self._format_hex_rows(self.xor_bytes_res)}")
        self.current_state = bytes_to_state(self.xor_bytes_res)
        self.state_text.delete('1.0', 'end')
        self.state_text.insert('end', state_to_hex(self.current_state))
        self.trace_text.insert('end', '[Langkah 2] XOR/AddRoundKey (Round 0) selesai. Lanjutkan Generate Key Schedule.\n\n')
        self.trace_text.see('end')

    def step_generate_keys(self):
        if self.key_bytes is None:
            messagebox.showinfo('Info', 'Lakukan Langkah 1 (Konversi) terlebih dahulu.')
            return
        kb = list(self.key_bytes) if isinstance(self.key_bytes, (bytes, bytearray)) else list(self.key_bytes)
        kb = (kb + [0] * 16)[:16]

        # gunakan versi trace
        self.round_keys, trace_lines = key_expansion_trace(kb)

        # tampilkan list round keys (ringkasan)
        self.keys_list.delete(0, 'end')
        for i, rk in enumerate(self.round_keys):
            self.keys_list.insert('end', f"Round {i}: " + bytes_to_hex(rk))

        # tampilkan trace detil di panel Trace
        self.trace_text.insert('end', '[Langkah 3] Pembangkitan kunci selesai. Detail ekspansi kunci:\n\n')
        for line in trace_lines:
            self.trace_text.insert('end', line + '\n')
        self.trace_text.insert('end', '\n')  # tambahan newline
        self.trace_text.see('end')

        # set current_state seperti semula
        if self.xor_bytes_res is not None:
            self.current_state = bytes_to_state(self.xor_bytes_res)
        else:
            pb = list(self.plain_bytes) if self.plain_bytes is not None else [0] * 16
            pb = (pb + [0] * 16)[:16]
            self.current_state = bytes_to_state(pb)
        # prepare to start round 1
        self.current_round = 1
        self.current_substep = 0

    # start_rounds used by UI button to ensure keys generated
    def start_rounds(self):
        if self.round_keys is None:
            messagebox.showinfo('Info', 'Lakukan Generate Key Schedule terlebih dahulu (Langkah 3).')
            return
        self.current_round = 1
        self.current_substep = 0
        self.trace_text.insert('end', f'---- Mulai Round {self.current_round} ----\n')
        self.trace_text.see('end')

    def next_substep(self):
        if self.round_keys is None:
            messagebox.showinfo('Info', 'Lakukan Langkah 3: Generate Key Schedule terlebih dahulu.')
            return
        if self.current_round > 10:
            messagebox.showinfo('Info', 'Semua ronde selesai.')
            return
        title = f"Round {self.current_round}"
        if self.current_substep == 0:
            self.trace_text.insert('end', f"=== {title} - SubBytes ===\n")
            self.current_state = sub_bytes(self.current_state)
            self.trace_text.insert('end', state_to_hex(self.current_state) + '\n\n')
        elif self.current_substep == 1:
            self.trace_text.insert('end', f"=== {title} - ShiftRows ===\n")
            self.current_state = shift_rows(self.current_state)
            self.trace_text.insert('end', state_to_hex(self.current_state) + '\n\n')
        elif self.current_substep == 2:
            if self.current_round == 10:
                self.trace_text.insert('end', f"=== {title} - MixColumns SKIPPED (Final Round) ===\n\n")
            else:
                self.trace_text.insert('end', f"=== {title} - MixColumns ===\n")
                self.current_state = mix_columns(self.current_state)
                self.trace_text.insert('end', state_to_hex(self.current_state) + '\n\n')
        elif self.current_substep == 3:
            self.trace_text.insert('end', f"=== {title} - AddRoundKey ===\n")
            rk = self.round_keys[self.current_round]
            self.trace_text.insert('end', 'Round key (hex): ' + bytes_to_hex(rk) + '\n')
            self.current_state = add_round_key(self.current_state, rk)
            self.trace_text.insert('end', state_to_hex(self.current_state) + '\n\n')
            self.state_text.delete('1.0', 'end')
            self.state_text.insert('end', state_to_hex(self.current_state))
        self.current_substep = (self.current_substep + 1) % 4
        self.trace_text.see('end')

    def next_round(self):
        if self.round_keys is None:
            messagebox.showinfo('Info', 'Generate keys terlebih dahulu.')
            return
        if self.current_round >= 10:
            messagebox.showinfo('Info', 'Round akhir sudah tercapai.')
            return
        self.current_round += 1
        self.current_substep = 0
        self.trace_text.insert('end', f'---- Mulai Round {self.current_round} ----\n')
        self.trace_text.see('end')

    def run_all_rounds(self):
        if self.round_keys is None:
            messagebox.showinfo('Info', 'Generate keys terlebih dahulu.')
            return
        start = max(1, self.current_round)
        for r in range(start, 11):
            # SubBytes
            self.current_state = sub_bytes(self.current_state)
            self.trace_text.insert('end', f"=== Round {r} - SubBytes ===\n{state_to_hex(self.current_state)}\n\n")
            # ShiftRows
            self.current_state = shift_rows(self.current_state)
            self.trace_text.insert('end', f"=== Round {r} - ShiftRows ===\n{state_to_hex(self.current_state)}\n\n")
            # MixColumns (skip for final round)
            if r != 10:
                self.current_state = mix_columns(self.current_state)
                self.trace_text.insert('end', f"=== Round {r} - MixColumns ===\n{state_to_hex(self.current_state)}\n\n")
            else:
                self.trace_text.insert('end', f"=== Round {r} - MixColumns SKIPPED ===\n\n")
            # AddRoundKey
            rk = self.round_keys[r]
            self.current_state = add_round_key(self.current_state, rk)
            self.trace_text.insert('end', f"=== Round {r} - AddRoundKey ===\nRound key: {bytes_to_hex(rk)}\n{state_to_hex(self.current_state)}\n\n")
        self.trace_text.insert('end', '--- Semua ronde selesai. Ciphertext (hex):\n' + bytes_to_hex(state_to_bytes(self.current_state)) + '\n')
        self.state_text.delete('1.0', 'end')
        self.state_text.insert('end', state_to_hex(self.current_state))
        self.trace_text.see('end')
        self.current_round = 11

    def run_all(self):
        self.step_convert()
        self.step_xor()
        self.step_generate_keys()
        self.run_all_rounds()

    def reset_all(self):
        self.plain_entry.delete(0, 'end')
        self.key_entry.delete(0, 'end')
        self.conv_plain.delete('1.0', 'end')
        self.conv_key.delete('1.0', 'end')
        self.xor_text.delete('1.0', 'end')
        self.keys_list.delete(0, 'end')
        self.state_text.delete('1.0', 'end')
        self.trace_text.delete('1.0', 'end')
        self.plain_bytes = None
        self.key_bytes = None
        self.xor_bytes_res = None
        self.round_keys = None
        self.current_round = 0
        self.current_substep = 0
        self.current_state = bytes_to_state([0] * 16)


# run
if __name__ == '__main__':
    try:
        app = AESVisualizer()
        app.mainloop()
    except Exception as e:
        print('Fatal error running GUI:', e)
