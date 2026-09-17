import random   
from dataMahasiswa import data
from fungsiMahasiswa import show_data, presensi_dummy, acak_data

data = data.copy()
presensi_dummy(data)
acak_data(data)



def sort_by(data: list=data, index: str="nim",rev = False):
    maps = {
        "nim":0,
        "nama":1,
        "presensi":2,
    }
    
    # Kerjakan disini
    n = maps [index]
    for i in range(len(data)-1):
        for j in range(len(data)-1-i):
            if rev == True:
                if data[j][n] < data[j + 1] [n]:
                    data[j], data[j+1]= data[j+1], data[j]
            else:
                if data[j][n]>data[j+1] [n]:
                    data[j], data[j+1] = data[j+1], data[j]

    # Jangan Dihapus
    show_data(data)

sort_by(data)


    
