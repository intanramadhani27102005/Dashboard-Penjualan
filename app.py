import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv

# =============================
# Fungsi Membaca CSV Manual
# =============================
def load_csv():
    file_path = filedialog.askopenfilename(
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
    )
    if not file_path:
        return

    try:
        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)

        if len(data) < 2:
            messagebox.showerror("Error", "CSV tidak memiliki data.")
            return

        headers = data[0]
        rows = data[1:]

        # bersihkan tabel lama
        for col in table.get_children():
            table.delete(col)

        table["columns"] = headers
        table["show"] = "headings"

        for col in headers:
            table.heading(col, text=col)
            table.column(col, width=120)

        for row in rows:
            table.insert("", tk.END, values=row)

        # hitung statistik
        hitung_statistik(rows)

        # buat grafik
        buat_grafik(rows)

    except Exception as e:
        messagebox.showerror("Error", f"Gagal membaca CSV: {e}")


# =============================
# Fungsi Menghitung Statistik
# =============================
def hitung_statistik(rows):
    try:
        total = 0
        for r in rows:
            total += float(r[-1])  # kolom terakhir dianggap penjualan

        jumlah = len(rows)
        rata = total / jumlah if jumlah > 0 else 0

        label_total.config(text=f"Total Penjualan: {total}")
        label_jumlah.config(text=f"Jumlah Transaksi: {jumlah}")
        label_rata.config(text=f"Rata-rata Penjualan: {rata:.2f}")

    except:
        messagebox.showerror("Error", "Kolom terakhir CSV harus berupa angka.")


# =============================
# Fungsi Membuat Grafik Bar
# =============================
def buat_grafik(rows):
    canvas.delete("all")

    if len(rows) == 0:
        return

    values = [float(r[-1]) for r in rows]
    max_val = max(values)

    w = 600
    h = 250
    bar_width = w / len(values)

    for i, val in enumerate(values):
        x0 = i * bar_width + 10
        y0 = h - (val / max_val * (h - 20))
        x1 = (i+1) * bar_width
        y1 = h

        canvas.create_rectangle(x0, y0, x1, y1, fill="#4A90E2")
        canvas.create_text(x0 + 20, y0 - 10, text=str(val), fill="black")


# =============================
# Setup Window
# =============================
root = tk.Tk()
root.title("Dashboard Penjualan Interaktif")
root.geometry("900x700")

# Tombol Load
btn_load = tk.Button(root, text="Upload CSV", command=load_csv, bg="#4CAF50", fg="white", font=("Arial", 12))
btn_load.pack(pady=10)

# Tabel
table_frame = tk.Frame(root)
table_frame.pack()

table = ttk.Treeview(table_frame)
table.pack()

# Statistik
stat_frame = tk.Frame(root)
stat_frame.pack(pady=10)

label_total = tk.Label(stat_frame, text="Total Penjualan: -", font=("Arial", 12))
label_total.pack()

label_jumlah = tk.Label(stat_frame, text="Jumlah Transaksi: -", font=("Arial", 12))
label_jumlah.pack()

label_rata = tk.Label(stat_frame, text="Rata-rata Penjualan: -", font=("Arial", 12))
label_rata.pack()

# Grafik
canvas = tk.Canvas(root, width=600, height=250, bg="white")
canvas.pack(pady=20)

root.mainloop()
