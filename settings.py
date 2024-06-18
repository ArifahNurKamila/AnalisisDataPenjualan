import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns

# Membaca dataset
penjualan_asli = pd.read_csv('penjualan_asli.csv')
penjualan_laporan = pd.read_csv('penjualan_laporan.csv')

# Menggabungkan kedua dataset berdasarkan 'tanggal' dan 'produk'
gabungan = pd.merge(penjualan_asli, penjualan_laporan, on=['tanggal', 'produk'], suffixes=('_asli', '_laporan'), how='outer', indicator=True)

# Menemukan perbedaan dalam jumlah terjual
perbedaan_jumlah = gabungan[gabungan['jumlah_terjual_asli'] != gabungan['jumlah_terjual_laporan']]

# Menemukan produk yang ada di satu dataset tetapi tidak ada di dataset lainnya
produk_berbeda = gabungan[gabungan['_merge'] != 'both']

# Menampilkan hasil analisis
print("Perbedaan dalam jumlah terjual:")
print(perbedaan_jumlah[['tanggal', 'produk', 'jumlah_terjual_asli', 'jumlah_terjual_laporan']])

print("\nProduk yang hanya ada di satu dataset:")
print(produk_berbeda[['tanggal', 'produk', '_merge']])

# Membuat grafik batang untuk perbedaan jumlah terjual
if not perbedaan_jumlah.empty:
    perbedaan_jumlah.set_index('tanggal')[['jumlah_terjual_asli', 'jumlah_terjual_laporan']].plot(kind='bar', figsize=(10, 6))
    plt.title('Perbedaan Jumlah Terjual')
    plt.ylabel('Jumlah Terjual')
    plt.xlabel('Tanggal')
    plt.show()
else:
    print("Tidak ada perbedaan jumlah terjual.")

    # Menambahkan grafik penjualan per produk
gabungan['jumlah_terjual_asli'].fillna(0, inplace=True)
gabungan['jumlah_terjual_laporan'].fillna(0, inplace=True)

penjualan_per_produk = gabungan.groupby('produk')[['jumlah_terjual_asli', 'jumlah_terjual_laporan']].sum()

penjualan_per_produk.plot(kind='bar', figsize=(10, 6))
plt.title('Penjualan Per Produk')
plt.ylabel('Jumlah Terjual')
plt.xlabel('Produk')
plt.xticks(rotation=45)
plt.show()

# Membuat grafik penjualan per tanggal
gabungan['tanggal'] = pd.to_datetime(gabungan['tanggal'])  # Pastikan kolom tanggal dalam format datetime
penjualan_per_tanggal = gabungan.groupby('tanggal')[['jumlah_terjual_asli', 'jumlah_terjual_laporan']].sum()
penjualan_per_tanggal.plot(kind='bar', figsize=(10, 6))
plt.title('Penjualan Per Tanggal')
plt.ylabel('Jumlah Terjual')
plt.xlabel('Tanggal')
plt.xticks(rotation=45)
plt.show()

# Menambahkan kolom regional untuk perbedaan_jumlah
perbedaan_jumlah = pd.merge(perbedaan_jumlah, penjualan_asli[['tanggal', 'produk', 'regional']], on=['tanggal', 'produk'], how='left')

# Grafik Perbedaan Penjualan per Regional
perbedaan_per_regional = perbedaan_jumlah.groupby('regional')[['jumlah_terjual_asli', 'jumlah_terjual_laporan']].sum().reset_index()

plt.figure(figsize=(10, 6))
bar_width = 0.35
index = range(len(perbedaan_per_regional))

plt.bar(index, perbedaan_per_regional['jumlah_terjual_asli'], bar_width, label='Asli')
plt.bar([i + bar_width for i in index], perbedaan_per_regional['jumlah_terjual_laporan'], bar_width, label='Laporan')

plt.xlabel('Regional')
plt.ylabel('Jumlah Terjual')
plt.title('Perbedaan Penjualan per Regional')
plt.xticks([i + bar_width / 2 for i in index], perbedaan_per_regional['regional'])
plt.legend()
plt.show()