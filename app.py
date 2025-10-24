import streamlit as st 
import pandas as pd
import os
import datetime

st.set_page_config(page_title="Bank Digital Anna 💵", layout="wide")

CSV_FILE = "ringkasan_nasabah.csv"

def memuat_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(Columns=["nama", "Total_Setor", "Total Ambil", "Saldo_Akhir", "Saldo Bersih", "Tanggal_Transaksi"])
    
def menyimpan_data(df):
    df.to_csv(CSV_FILE, index=False)

df = memuat_data()

st.title("🏦 Aplikasi Bank Digital Anna")

menu = st.sidebar.radio(
    "Home",
    ["📋 Lihat Semua Nasabah", "➕ Tambah / Update Nasabah", "💸 Setor / Ambil Uang", "❌ Hapus Nasabah"]
)

# =====================================================
# 1️⃣ LIHAT SEMUA NASABAH
# =====================================================

if menu == "📋 Lihat Semua Nasabah":
    st.subheader("📊 Daftar Nasabah dan Saldo Terakhir")
    st.dataframe(df, use_container_width=True)

# =====================================================
# 2️⃣ TAMBAH / UPDATE NASABAH
# =====================================================

elif menu == "➕ Tambah / Update Nasabah":
    st.subheader("➕ Tambah atau Update Nasabah Baru")

    nama= st.text_input("Nama Nasabah:")
    setor_awal = st.number_input("Setoran Awal (Opsional)", min_value=0, value=0, step=1000)

    if st.button("Simpan Data"):
        if nama == "":
            st.warning("Nama tidak boleh kosong!")
        else:
            if nama in df["nama"].values:
                st.info(f"Nasabah **{nama}** sudah ada, datanya akan diperbarui.")
                df.loc[df["nama"] == nama, "Total_Setor"] += setor_awal
                df.loc[df["nama"] == nama, "Saldo_Akhir"] += setor_awal
                df.loc[df["nama"] == nama, "Saldo_Bersih"] += setor_awal
            else:
                new_row = pd.DataFrame({
                    "nama" : [nama],
                    "Total_Setor" : [setor_awal],
                    "Total_Ambil" : [0],
                    "Saldo_Akhir" : [setor_awal],
                    "Saldo_Bersih" : [setor_awal],
                    "Tanggal_Transaksi": [datetime.date.today()]
                })
                df = pd.concat([df, new_row],ignore_index=True)

            menyimpan_data(df)
            st.success(f"Data Nasabah **{nama}** berhasil disimpan!")

# =====================================================
# 3️⃣ SETOR / AMBIL UANG
# =====================================================

elif menu == "💸 Setor / Ambil Uang":
    st.subheader("💰 Transaksi Setor / Ambil Uang")

    if len(df) == 0:
        st.warning("Belum ada nasabah.")
    else:
        for col in ["Total_Setor", "Total_Ambil", "Saldo_Akhir", "Saldo_Bersih"]:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

        nama = st.selectbox("Pilih Nasabah", df["nama"].unique())
        jenis = st.radio("Jenis Transaksi", ["Setor", "Ambil"])
        jumlah = st.number_input("Jumlah", min_value=1000, step=1000)

        if st.button("Simpan Transaksi"):
            idx = df[df["nama"] == nama].index[0]

            total_setor = df.at[idx, "Total_Setor"]
            total_ambil = df.at[idx, "Total_Ambil"]
            saldo_akhir = df.at[idx, "Saldo_Akhir"]

            if jenis == "Setor":
                total_setor += jumlah
                saldo_akhir += jumlah
                st.success(f"✅ {nama} setor Rp{jumlah:,}")
            else:  
                if jumlah > saldo_akhir:
                    st.error("❌ Saldo tidak mencukupi untuk penarikan!")
                else:
                    total_ambil += jumlah
                    saldo_akhir -= jumlah
                    st.success(f"✅ {nama} ambil Rp{jumlah:,}")

            df.at[idx, "Total_Setor"] = total_setor
            df.at[idx, "Total_Ambil"] = total_ambil
            df.at[idx, "Saldo_Akhir"] = saldo_akhir
            df.at[idx, "Saldo_Bersih"] = total_setor - total_ambil

            df.at[idx, "Tanggal_Transaksi"] = datetime.date.today()
            menyimpan_data(df)
            st.info(f"Saldo {nama} sekarang: Rp{saldo_akhir:,}")

# =====================================================
# 4️⃣ HAPUS NASABAH
# =====================================================

elif menu == "❌ Hapus Nasabah":
    st.subheader("🗑️ Hapus Data Nasabah")

    if len(df) == 0:
        st.warning("⚠️ Belum ada nasabah untuk dihapus.")
    else:
        nama = st.selectbox("Pilih Nasabah yang akan dihapus", df["nama"].unique())

        if st.button("Hapus Nasabah"):
            df = df[df["nama"] !=nama]
            menyimpan_data(df)
            st.success(f"✅ Data nasabah **{nama}** berhasil dihapus!")

# =====================================================
# Footer
# =====================================================
st.markdown("---")
st.caption("💻 Dibuat oleh Anna 🐤")