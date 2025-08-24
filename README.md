Gaturu — COMPFEST 17 Submission
Deskripsi Singkat

Repository ini berisi kode dan dokumen pendukung untuk proyek Gaturu, sebuah sistem deteksi microsleep berbasis IoT dengan integrasi Machine Learning dan sensor MPU-6050. Proyek ini diajukan dalam rangka kompetisi COMPFEST 17.

Struktur Repository

AI_MODEL/
Folder ini merupakan arsip lama dari eksperimen awal pengembangan model. Tidak digunakan dalam implementasi akhir.

(Root Repository)
Seluruh file utama yang relevan untuk penilaian tersedia langsung di root repository, tanpa perlu masuk ke dalam folder tambahan.

Penjelasan File Utama

ws_server.py
File inti yang harus dijalankan oleh juri. File ini:

Membuka WebSocket server untuk menerima data sensor dari ESP32 + MPU-6050.

Menerapkan logika deteksi microsleep menggunakan kombinasi aturan threshold dan filter Machine Learning.

Mengirimkan status (AWAKE atau MICROSLEEP) kembali ke client, sekaligus mengaktifkan buzzer ketika microsleep terdeteksi.

Menyediakan antarmuka dashboard sederhana agar status dapat dipantau secara langsung.

microsleep_model.pkl dan scaler.pkl
Model Machine Learning yang sudah dilatih beserta skaler untuk normalisasi data. Keduanya dimuat otomatis oleh ws_server.py.

train_microsleep_az_only.py
Script untuk melatih ulang model berbasis data sumbu Z (az) dari MPU-6050. Tidak perlu dijalankan kecuali jika juri ingin mereplikasi proses pelatihan.

dataset.csv
Dataset contoh yang digunakan dalam proses pelatihan model.

Instruksi Bagi Juri

Pastikan perangkat IoT (ESP32 dengan sensor MPU-6050 dan buzzer aktif) sudah dikonfigurasi sesuai instruksi teknis.

Clone repository ini ke komputer lokal.

Dari root repository, jalankan perintah berikut:

python ws_server.py


Sistem akan memulai WebSocket server. Saat perangkat IoT terhubung dan mengirimkan data sensor, status akan otomatis ditampilkan di terminal maupun dashboard sederhana.

Jika microsleep terdeteksi, buzzer akan aktif, indikator status akan berubah menjadi "MICROSLEEP", dan jumlah episode microsleep akan tercatat.

Catatan

Folder AI_MODEL/ tidak digunakan dalam implementasi akhir.

Seluruh file yang diperlukan untuk menjalankan proyek sudah tersedia langsung di root repository.

Sistem membutuhkan koneksi jaringan agar komunikasi WebSocket antara ESP32 dan server berjalan dengan baik.
