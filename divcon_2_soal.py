# Data mahasiswa dan 5 nilai UG
mahasiswa = [
    {"nama": "Andi", "nilai": [80, 75, 90, 70, 85]},
    {"nama": "Budi", "nilai": [60, 65, 70, 55, 60]},
    {"nama": "Citra", "nilai": [90, 85, 95, 88, 92]},
    {"nama": "Deni", "nilai": [70, 75, 65, 72, 68]},
    {"nama": "Eka", "nilai": [85, 80, 78, 90, 87]},
    {"nama": "Fajar", "nilai": [65, 70, 68, 60, 72]},
    {"nama": "Gina", "nilai": [88, 92, 85, 90, 87]},
    {"nama": "Hadi", "nilai": [75, 80, 70, 78, 72]},
    {"nama": "Intan", "nilai": [55, 60, 65, 58, 62]},
    {"nama": "Joko", "nilai": [78, 82, 75, 80, 85]}
]


# Menghitung rata-rata nilai setiap mahasiswa
for mhs in mahasiswa:
    total = 0 
    for nilai in mhs["nilai"]:
        total += nilai 
    mhs["rata-rata"] = total / len(mhs["nilai"])
    
    
    

# Divide and Conquer - Merge Sort
def merge_sort(data):
    if len(data) <= 1:
        return data
    tengah = len(data) // 2
    kiri = merge_sort(data[:tengah])
    kanan = merge_sort(data[tengah:])
    return merge(kiri, kanan)

   
def merge(kiri, kanan):
    hasil = []
    i = 0 
    j = 0
    while i<len(kiri)and j<len(kanan):
        if kiri[i]["rata-rata"]>kanan[j]["rata-rata"]:
            hasil.append(kiri[i])
            i+=1
        else:
            hasil.append(kanan[j])
            j+=1
    hasil.extend(kiri[i:])
    hasil.extend(kanan[j:])
    return hasil
    

# Menghitung rata-rata keseluruhan
total = 0 
for mhs in mahasiswa: 
    total += mhs["rata-rata"]
keseluruhan = total // len(mahasiswa)


# Mengurutkan mahasiswa menggunakan Merge Sort
mahasiswa_urut = merge_sort(mahasiswa)
atas = []
bawah = []

for mhs in mahasiswa_urut:
    if mhs["rata-rata"] >= keseluruhan:
        atas.append(mhs)
    else:
        bawah.append(mhs)

# Menampilkan hasil rata-rata keseluruhan


print("\n=== DI ATAS / SAMA DENGAN RATA-RATA ===")

# Tampilkan List di atas / sama dengan rata-rata
num = 1
for mhs in mahasiswa_urut:
    if mhs["rata-rata"]>= keseluruhan:
        print(num, ".", mhs["nama"], "- Nilai:", mhs["nilai"], "- rata-rata:", mhs["rata-rata"])
        num +=1
        


print("\n=== DI BAWAH RATA-RATA ===")

# Tampilkan List di bawah rata-rata
num = 1
for mhs in mahasiswa_urut:
    if mhs["rata-rata"]< keseluruhan:
        print(num, ".", mhs["nama"], "- Nilai:", mhs["nilai"], "- rata-rata:", mhs["rata-rata"])
        num +=1
        