import streamlit as st
import csv

st.set_page_config(page_title="Dashboard Penjualan Interaktif", layout="wide")

st.title("📊 Dashboard Penjualan Interaktif (Tanpa Pandas)")

# ============================
# Fungsi Membaca CSV Manual
# ============================
def baca_csv(file):
    file_data = file.read().decode("utf-8").splitlines()
    reader = csv.reader(file_data)
    data = list(reader)
    return data


# ============================
# Upload File
# ============================
file = st.file_uploader("Upload file CSV penjualan", type=["csv"])

if file:
    data = baca_csv(file)

    # Pastikan data valid
    if len(data) < 2:
        st.error("CSV tidak memiliki data!")
        st.stop()

    header = data[0]
    rows = data[1:]

    # ============================
    # Tampilkan Data
    # ============================
    st.subheader("📌 Data Penjualan")
    st.table(data)

    # ============================
    # Hitung Statistik
    # ============================
    try:
        nilai_penjualan = [float(r[-1]) for r in rows]
        total = sum(nilai_penjualan)
        jumlah = len(nilai_penjualan)
        rata = total / jumlah if jumlah > 0 else 0

        st.subheader("📈 Statistik Penjualan")
        col1, col2, col3 = st.columns(3)

        col1.metric("Total Penjualan", f"{total:,.2f}")
        col2.metric("Jumlah Transaksi", jumlah)
        col3.metric("Rata-rata Penjualan", f"{rata:,.2f}")

    except:
        st.error("Kolom terakhir CSV harus berupa angka.")
        st.stop()

    # ============================
    # Grafik Penjualan
    # ============================
    st.subheader("📊 Grafik Penjualan per Transaksi")
    st.line_chart(nilai_penjualan)

else:
    st.info("Silakan upload file CSV terlebih dahulu.")
