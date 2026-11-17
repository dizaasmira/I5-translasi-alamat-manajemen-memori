# translasi_alamat.py - I-5 Translasi Alamat dan Manajemen Memori
import math

KB, MB, GB = 1024, 1024**2, 1024**3
ALAMAT = [8192, 50000, 2097152]
UKURAN_PAGE = {"4 KB": 4*KB, "2 MB": 2*MB}

# ASUMSI: nomor frame hipotetis hasil pemetaan page table (tidak diberikan di soal)
FRAME = {
    "4 KB": {2: 7, 12: 20, 512: 1030},
    "2 MB": {0: 3, 1: 5},
}

print("=== 1. Translasi alamat logis -> fisik ===")
for nama, ps in UKURAN_PAGE.items():
    print(f"\nUkuran page {nama} = {ps} byte")
    for a in ALAMAT:
        p, d = divmod(a, ps)
        f = FRAME[nama][p]
        fisik = f * ps + d
        print(f"  logis {a:>8}: page={p:<4} offset={d:<8} frame={f:<5} fisik={f}*{ps}+{d} = {fisik}")

print("\n=== 2. TLB reach ===")
for entri in (64, 1536):
    for nama, ps in UKURAN_PAGE.items():
        r = entri * ps
        print(f"  {entri:>4} entri x {nama}: {r} byte = {r/KB:.0f} KB = {r/MB:.2f} MB")

print("\n=== 3. Effective Access Time (eps=10 ns, m=100 ns, 1 level) ===")
eps, m = 10, 100
for h in (0.80, 0.90, 0.95, 0.99):
    eat = h*(eps+m) + (1-h)*(eps+2*m)
    print(f"  hit ratio {h*100:.0f}% -> EAT = {eat:.1f} ns  (slowdown {eat/m:.2f}x terhadap m)")
print("  Skenario banding (4-level vs 3-level walk):")
e4 = 0.90*(eps+m) + 0.10*(eps+5*m)
e2 = 0.99*(eps+m) + 0.01*(eps+4*m)
print(f"    4 KB, hit 90%: EAT = {e4:.1f} ns")
print(f"    2 MB, hit 99%: EAT = {e2:.1f} ns")

print("\n=== 4. Ukuran page table ===")
for nama, ps in UKURAN_PAGE.items():
    n32 = 2**32 // ps
    nbuf = 16*GB // ps
    print(f"  {nama}: 32-bit/PTE 4B  -> {n32} entri = {n32*4/KB:.0f} KB ({n32*4/MB:.3f} MB)")
    print(f"  {nama}: buffer 16 GB/PTE 8B -> {nbuf} entri = {nbuf*8/MB:.3f} MB")

print("\n=== 5. Fragmentasi internal ===")
for ukuran in (2097153, 5_000_000):
    for nama, ps in UKURAN_PAGE.items():
        n = math.ceil(ukuran/ps)
        sisa = n*ps - ukuran
        print(f"  alokasi {ukuran} B, page {nama}: {n} page, sisa {sisa} B ({sisa/ps*100:.1f}% dari 1 page)")
