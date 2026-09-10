def pirangka(angka):
    for baris in range(1, angka + 1):
        jarak = "  " * (angka - baris)
        up = " ".join(str(i) for i in range(1, baris + 1))
        down = " ".join(str(i) for i in range(baris - 1, 0, -1))
        if up:
            print(jarak + up + " " + down)
        else:
            print(jarak + up)

pirangka(3)







