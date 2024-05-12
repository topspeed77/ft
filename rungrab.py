import os

print("Welcome to Ftp Tools Anjay")
print("Pilih Lah:")
print("1. Ftp Grab")
print("2. Ftp Split")
print("3. Ftp Cek")

def screen_clear():
    os.system('cls')
# Input pilihan pengguna
pilihan = input("Masukan Pilihan Angka 1, 2, atau 3: ")

# Cek input pengguna dan jalankan file yang sesuai
if pilihan == "1":
    os.system("python script/ftprun.py")
elif pilihan == "2":
    os.system("python script/ftpsplit.py")
elif pilihan == "3":
    os.system("python script/ftpcheck.py")
else:
    print("Pilihan tidak valid. Silakan masukkan angka 1, 2, atau 3.")
