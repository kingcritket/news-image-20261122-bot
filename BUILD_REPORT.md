# BUILD REPORT — news-image-20261122 ("Sunday, In Full")

Repo: `~/workspace/makefun/news-image-20261122-bot/` — TIDAK di-submit /
TIDAK di-push (diserahkan ke parent agent).

## Hasil akhir

- `entry.png`: 1024×1024, 675.622 byte (di bawah 1 MiB)
- sha256 (build 2x byte-identik): `2f829e67e015de652cc04f40eab3d6d22813a65cdccb3a03e39f1beafa920645`
- `main.py` 2x byte-identik (sha256 sama dengan entry.png)
- Runtime tanpa jaringan: hanya `os` + PIL (build_entry.py),
  `os/shutil/sys` (main.py); tanpa random/time
- Cek visual ukuran penuh + 300px: bersih setelah 2 putaran perbaikan
- Kit TIDAK menyediakan grade-local untuk bounty ini (RULES.txt:
  "There is no local grade of this competition: the server grades
  every entry") — tidak ada yang bisa dijalankan lokal selain build +
  main.py.
- 32 berita ber-tanggal, semua kejadian / pertama dilaporkan
  22 November 2026 di suatu zona waktu (lihat "Date discipline" di
  README.md).

## Ringkasan konsep

Front-page koran "SUNDAY, IN FULL" dengan identitas visual Brief #2
pengguna (Sunlit Crime-Noir): kertas pasir hangat terang, masthead
hitam arang, aksen merah menyala, garis diagonal tajam (pembatas miring
merah di masthead + garis merah di atas tiap foto), tipografi bold
tegas. Lead: serangan semalam Rusia ke Ukraina (~550 munisi, 5 tewas)
dengan foto fajar Lviv. Dua kartu foto: COP31 Antalya (aula sidang
terik matahari, bayangan diagonal keras) dan peretasan database FBI
(kantor siang terik, bayangan bilah jendela). Grid "ALSO TODAY"
27 berita lintas 6 region + strip "BY THE NUMBERS".

## Keunggulan duel pairwise vs top 10

1. **Identitas visual yang langsung dikenali saat duel 1-lawan-1.**
   Top 10 saat ini semuanya koran abu-abu generik yang padat tapi
   tanpa karakter. Entry ini memakai palet pasir/hitam/merah yang sama
   di seluruh halaman (masthead, ticker, garis foto, kicker grid),
   sehingga di thumbnail 300px pun langsung beda dari koran abu-abu.
2. **Tanggal dan hari mustahil terlewat.** "SUNDAY, IN FULL" +
   "22 NOVEMBER 2026" + "32 DATED STORIES • 6 REGIONS" ada di
   masthead, ticker mengulang 4 berita utama, dan grid memakai header
   "ALSO TODAY — SUNDAY 22 NOVEMBER 2026". Juri (kriteria #1: nama
   hari + kejadian spesifik hari itu) langsung melihat ini hari
   Minggu 22 Nov 2026.
3. **Disiplin tanggal yang bisa dipertahankan.** Setiap berita
   diverifikasi tanggalnya lewat pencarian (BBC/Reuters/AP/dll);
   berita besar 20–21 Nov (Sinaloa, Bahrain, Bolsonaro, EU–Indonesia,
   gempa Peru & Timor, protes Prancis, dll) sengaja TIDAK dipakai
   walau entry teratas tampaknya memakainya — jadi tidak ada satu pun
   item yang juri bisa kenali sebagai berita hari lain.

## Berita final (32; semua 22 Nov 2026)

Lead: serangan semalam Rusia (~550 munisi: 496 drone + 53 rudal;
5 tewas, 10 luka; keluarga 4 orang di Lapaivka; Zaporizhzhia 1 tewas;
439 drone + 39 rudal ditembak jatuh). Kartu: COP31 (teks revisi
diajukan, Kurum: celah menyempit, pleno 10:00, bahan bakar fosil
tetap, 1.5°C sudah diakui terlewat) dan FBI (peretasan database
kriminal NCIC). Grid 27: Hong Kong, Nepal, AUKUS, Gaza aid,
Venezuela, Israel, Gulf, F1, Ashes, NFL, Cricket, Iran web,
COP31 AI, Qeshm, Oman, SCO, Prancis (Depardieu), Snooker, IFFI,
Hormuz, Chips, Gaza (129 jenazah), Somalia, Climate tech,
Victoria, Australia, New York. Strip 2: Panama (blokir deal COP31
tanpa bahasa fosil) + AAA (81,5 jt pelancong Thanksgiving).

## Foto adegan baru (AI-generated, tanpa teks di dalam foto)

1. `assets/media-generation-lviv-dawn-strike-0-543a3a0c-7105-40b3-812e-411fb98e62f1.webp`
   — gedung apartemen Lviv rusak berasap saat fajar, truk pemadam
2. `assets/media-generation-cop31-antalya-hall-0-3d974eb3-5cfb-4f9a-b064-63dad4043d89.webp`
   — aula pleno COP31 Antalya yang disinari matahari, bayangan diagonal
3. `assets/media-generation-fbi-office-sunlit-0-6f182ca9-4ebd-4d44-8511-3e9adddc9c75.webp`
   — kantor pemerintah siang terik, layar biru kosong, bayangan bilah

## Cacat yang diperiksa dan diperbaiki (cek visual 2 putaran)

1. **Paragraf lead ke-3 terpotong / menabrak baris kartu foto**
   (putaran 1): headline "RUSSIA'S NEW / OVERNIGHT BARRAGE" di 33pt
   ternyata memakan 3 baris ("OVERNIGHT BARRAGE" = 372px > lebar panel
   352px), mendorong badan lead ke bawah hingga paragraf ke-3
   tertimpa foto kartu. Diperbaiki: headline jadi 30pt (terukur
   338px, muat 2 baris) — paragraf ke-3 kini tampil penuh.
2. **Garis diagonal merah masthead menabrak blok tanggal**
   (putaran 1): dua poligon diagonal besar (x 736–908) melintasi teks
   "SUNDAY / 22 NOVEMBER 2026 / 32 DATED STORIES". Diperbaiki:
   diganti satu pembatas miring merah di x 636–664, di antara judul
   dan blok tanggal — tanggal kini bersih dan terbaca penuh.
3. Setelah perbaikan (putaran 2): ukuran penuh bersih — tidak ada teks
   meluber/terpotong/menabrak, foto tidak terpotong aneh, kontras
   baik; 300px terbaca (masthead, tanggal, headline lead, foto,
   kicker kartu jelas).

## Tes yang dijalankan

- `python3 build_entry.py` 2x: byte-identik (sha256 sama),
  1024×1024, 675.622 byte < 1 MiB.
- `MAKEFUN_OUTPUT_DIR=out python3 main.py`: menyalin entry.png
  byte-identik ke `out/entry.png`.
- Cek visual: ukuran penuh + 300px, 2 putaran (lihat atas).
- Grade-local: TIDAK TERSEDIA untuk bounty ini (dinyatakan di
  RULES.txt kit) — tidak dijalankan.
- Tidak ada grid item yang meluber ke 3 baris (peringatan runtime
  tidak muncul).

## Catatan / batasan

- Build dikerjakan ~02:00–03:00 UTC 22 Nov, jadi berita yang dipakai
  adalah yang terverifikasi sampai jam itu. Berita sore hari 22 Nov
  (hasil pleno COP31, hasil F1 Las Vegas GP, hasil pemilu Hong Kong,
  berita Minggu malam AS) BELUM ada saat build — refresh di siang/sore
  hari sebelum deadline (24 Nov 00:00 UTC) bisa menambah 5+ berita.
- Jumlah berita 32 (bukan 35+): aturan tanggal ketat membuat banyak
  berita besar 21 Nov harus dicoret; daftar yang dicoret ada di
  README.md ("Date discipline") agar parent bisa memutuskan sendiri
  bila ingin menambahkannya.
- TIDAK di-submit, TIDAK di-push ke GitHub — sesuai tugas.
