# Arsipal

Arsip surat PDF dengan pencarian metadata, dashboard, dan riwayat login.
Dibangun dengan Django dan SQLite; bisa dijalankan lewat Docker.

![Django 5.1.2](https://img.shields.io/badge/Django-5.1.2-092E20?logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white)
![Docker Compose](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)

## ✨ Yang bisa dilakukan

- Simpan, ubah, hapus, dan unduh surat PDF.
- Cari surat berdasarkan nomor, perihal, sifat, atau tanggal.
- Lengkapi metadata: tanggal surat, nomor, sifat, klasifikasi, dan perihal.
- Lihat jumlah arsip, kategori sifat surat, grafik bulanan, dan riwayat login.

Nomor, sifat, dan perihal dicoba dibaca dari teks PDF saat kolomnya kosong.
Periksa kembali hasilnya. **PDF scan tanpa teks belum didukung OCR.**

## 🚀 Menjalankan

Siapkan Docker Desktop dengan Linux containers. Dari folder proyek:

```powershell
docker compose up -d --build
docker compose ps
```

Startup menjalankan migrasi dan collectstatic secara otomatis. Setelah `web`
healthy, buat akun pertama:

```powershell
docker compose exec web python manage.py createsuperuser
```

Buka **[localhost:8001/login/](http://localhost:8001/login/)**.
Tidak ada akun bawaan. Setelah login, tambahkan PDF, periksa metadata, lalu simpan.

> Pengaturan bawaan ditujukan untuk penggunaan lokal. Database dan dokumen lama
> tidak otomatis diimpor ke volume Docker.

## 🔧 Panduan tambahan

<details>
<summary>Konfigurasi port dan environment</summary>

Jika ingin mengatur konfigurasi, siapkan `.env` sebelum startup:

```powershell
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
```

| Variabel | Kegunaan |
| --- | --- |
| `WEB_PORT` | Port browser; bawaan `8001`, terikat ke loopback |
| `DJANGO_SECRET_KEY` | Secret Django; ganti placeholder contoh |
| `DJANGO_DEBUG` | Mode debug; bawaan Compose `false` |
| `DJANGO_ALLOWED_HOSTS` | Host yang diizinkan mengakses aplikasi |

Di Docker, database berada di `/app/data/db.sqlite3` dan PDF di `/app/dokumen`.
Lokasinya diatur melalui `DATABASE_PATH` dan `MEDIA_ROOT` pada Compose.

</details>

<details>
<summary>Stop, rebuild, dan penyimpanan data</summary>

| Kebutuhan | Perintah |
| --- | --- |
| Menyalakan kembali | `docker compose up -d` |
| Menghentikan | `docker compose stop` |
| Menerapkan perubahan kode/dependensi | `docker compose up -d --build` |
| Membaca log | `docker compose logs --tail=100 web` |

Volume `sqlite_data` menyimpan database, sedangkan `document_data` menyimpan PDF.
Stop, rebuild, dan `docker compose down` mempertahankannya.
**`docker compose down -v` menghapus keduanya.**

Cadangkan database dan dokumen sebagai satu kesatuan. Jika berpindah dari instalasi
lama, cadangkan `db.sqlite3` dan folder `dokumen` sebelum memindahkannya secara sengaja.

</details>

<details>
<summary>Struktur kode dan pemeriksaan</summary>

| Lokasi | Isi |
| --- | --- |
| `arsip/` | Settings dan URL utama Django |
| `arsip_database/` | Model arsip, riwayat login, migrasi, dan test |
| `arsip_ui/` | Halaman, formulir, template, dan aset |
| `docker/` | Entrypoint container |

```powershell
docker compose exec web python manage.py check
docker compose exec web python manage.py test arsip_database
```

Test mencakup login, dashboard, riwayat login, metadata, dan unduh PDF dari lokasi
media terpisah. Healthcheck memeriksa halaman login. Jika startup gagal, periksa
log migrasi. Gunicorn memakai satu worker dan dua thread untuk penggunaan SQLite
lokal; Django tetap pada versi 5.1.2.

</details>
